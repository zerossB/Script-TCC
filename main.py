import time

from app.csv import Xcsv
from app.graphql import GraphQL
from app.html import HTML
from app.http import Http
from app.xlsx import Xlsx


def main():
    inicial = time.time()

    licenses = [
        "apache-2.0",
        "gpl-3.0",
        "mit",
    ]

    for license in licenses:
        csv = Xcsv(f"{license}")
        repos = csv.loadCsv()
        jsons = []

        graph = GraphQL("repository")
        busca = GraphQL("search")
        http = Http()
        html = HTML()
        xlsx = Xlsx(f"{license}")

        print(busca.readFile(license=f"{license}"))
        buscas = http.postGql(busca.readFile(license=f"{license}"))
        print(buscas['data']['search']['repositoryCount'])

        # Pegando Informações da API
        for rep in repos:
            print("> {}/{}".format(rep[0], rep[1]))
            text = graph.readFile(owner=rep[0], repo=rep[1])
            json = http.postGql(text)
            print(json, "\n")
            jsons.append(json)

        # Headers
        header = (
            'repositorio',
            'forks',
            'watchers',
            'stars',
            'commits',
            'contributors',
            'branches',
            'releases',
            'issue_open',
            'issue_closed',
            'issue_media_open',
            'issue_media_closed',
            'issue_total',
            'pull_open',
            'pull_closed',
            'pull_merged',
            'pull_media_open',
            'pull_media_closed',
            'pull_media_merged',
            'pull_total',
            'total'
        )

        repos = []
        # Preparando Lista para monitoração
        for rep in jsons:
            issue_open = rep['data']['repository']['issue_open']['totalCount']
            issue_closed = rep['data']['repository']['issue_closed']['totalCount']
            issue_total = issue_open + issue_closed
            if issue_total == 0:
                issue_total = 1

            pull_open = rep['data']['repository']['pull_open']['totalCount']
            pull_closed = rep['data']['repository']['pull_closed']['totalCount']
            pull_merged = rep['data']['repository']['pull_merged']['totalCount']
            pull_total = pull_open + pull_merged + pull_closed
            if pull_total == 0:
                pull_total = 1

            # repos.append(
            #     [
            #         rep['data']['repository']['nameWithOwner'],
            #         rep['data']['repository']['forkCount'],
            #         rep['data']['repository']['watchers']['totalCount'],
            #         rep['data']['repository']['stargazers']['totalCount'],
            #         rep['data']['repository']['commits']['history']['totalCount'],
            #     ]
            # )

            # Pegando HTML para Scrapping
            resp = http.getHTML(rep['data']['repository']['nameWithOwner'])
            contributors = html.getContributors(resp)

            repos.append(
                (
                    rep['data']['repository']['nameWithOwner'],
                    rep['data']['repository']['forkCount'],
                    rep['data']['repository']['watchers']['totalCount'],
                    rep['data']['repository']['stargazers']['totalCount'],
                    0 if rep['data']['repository']['commits'] is None else rep['data']['repository']['commits']['history']['totalCount'] ,
                    contributors,
                    rep['data']['repository']['branches']['totalCount'],
                    rep['data']['repository']['releases']['totalCount'],
                    issue_open,
                    issue_closed,
                    float(issue_open / issue_total),
                    float(issue_closed / issue_total),
                    issue_total,
                    pull_open,
                    pull_closed,
                    pull_merged,
                    float(pull_open / pull_total),
                    float(pull_closed / pull_total),
                    float(pull_merged / pull_total),
                    pull_total,
                    buscas['data']['search']['repositoryCount']
                )
            )
        xlsx.saveToWorkbook(header=header, data=repos)

        print("Esperando por 60s")
        time.sleep(60)

    final = time.time()
    print("> Tempo de Execução: %ss" % (final-inicial))


if __name__ == "__main__":
    main()
