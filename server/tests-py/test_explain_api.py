from validate import check_query_f
import pytest
import ruamel.yaml as yaml

usefixtures = pytest.mark.usefixtures


def url(hge_ctx):
    return hge_ctx.hge_url + '/v1/graphql/explain'


@usefixtures('per_class_tests_db_state')
class TestV1SelectBasic:

    def test_select_query_author(self, hge_ctx):

        f = self.dir() + 'select_query_user.yaml'
        with open(f, 'r+') as c:
            yml = yaml.YAML()
            conf = yml.load(c)
            query = conf['query']
            resp = hge_ctx.http.post(url(hge_ctx), json={'query': query})
            assert resp.status_code == 200

            plans = resp.json()
            assert type(plans) is list
            assert len(plans) == 1

            plan = plans[0]
            assert type(plan['field']) is str
            assert type(plan['sql']) is str

            postgres_plan = plan['plan']
            assert type(postgres_plan) is list

    @classmethod
    def dir(cls):
        return "queries/graphql_query/basic/"
