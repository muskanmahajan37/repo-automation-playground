import constants
import source_parser
import unittest


class ParserSmokeTests(unittest.TestCase):
    def test_direct_invocation_parser(self):
        source_path = 'test_data/parser/http/http_main.py'

        source_methods = source_parser.get_top_level_methods(source_path)
        source_methods = [x for x in source_methods if
                          x.drift['parser'] == 'direct_invocation']

        source_region_tags = source_parser.get_region_tag_regions(source_path)
        source_parser.add_region_tags_to_methods(
            source_methods, source_region_tags)

        assert len(source_methods) == 9
        method = source_methods[0]
        assert hasattr(method, 'drift')
        assert method.drift['name'] == 'hello_get'
        assert 'functions_helloworld_get' in method.drift['region_tags']

    def test_webapp2_parser(self):
        source_path = 'test_data/parser/webapp2/webapp2_main.py'

        source_methods = source_parser.get_top_level_methods(source_path)
        source_methods = [x for x in source_methods if
                          x.drift['parser'] == 'webapp2_router']

        source_region_tags = source_parser.get_region_tag_regions(source_path)
        source_parser.add_region_tags_to_methods(
            source_methods, source_region_tags)

        assert len(source_methods) == 3

        method = source_methods[-1]
        assert hasattr(method, 'drift')
        assert method.drift['url'] == '/sign'

        assert method.drift['http_method'] == 'post'
        self.assertEqual(method.drift['region_tags'], ['sign_handler'])

    def test_flask_router_parser(self):
        source_path = 'test_data/parser/flask/flask_main.py'

        source_methods = source_parser.get_top_level_methods(source_path)
        source_methods = [x for x in source_methods if
                          x.drift['parser'] == 'flask_router']

        source_region_tags = source_parser.get_region_tag_regions(source_path)
        source_parser.add_region_tags_to_methods(
            source_methods, source_region_tags)

        # direct_invocation parser should ignore Flask methods
        assert len(source_methods) == 1

        method = source_methods[0]
        assert hasattr(method, 'drift')
        assert method.drift['url'] == '/'

        # Flask has a default HTTP method set for routes that don't specify any
        assert method.drift['http_methods'] == constants.FLASK_DEFAULT_METHODS

        self.assertEqual(method.drift['region_tags'], ['sample_route'])


class ParserEdgeCaseTests(unittest.TestCase):
    def test_ignores_ignored_method_names(self):
        source_path = 'test_data/parser/edge_cases/edge_cases.py'

        source_methods = source_parser.get_top_level_methods(source_path)

        source_region_tags = source_parser.get_region_tag_regions(source_path)
        source_parser.add_region_tags_to_methods(
            source_methods, source_region_tags)

        assert len(source_methods) == 1
        method = source_methods[0]
        assert hasattr(method, 'drift')

        print(method.drift)
        assert method.drift['name'] == 'not_main'

        # this should NOT contain 'main_method'
        self.assertEqual(method.drift['region_tags'], ['not_main'])

    def test_region_tags_nested(self):
        source_path = 'test_data/parser/nested_tags/nested_tags.py'

        source_methods = source_parser.get_top_level_methods(source_path)

        source_region_tags = source_parser.get_region_tag_regions(source_path)
        source_parser.add_region_tags_to_methods(
            source_methods, source_region_tags)

        method_1 = source_methods[0]
        method_2 = source_methods[1]

        assert hasattr(method_1, 'drift')
        assert hasattr(method_2, 'drift')

        assert method_1.drift['name'] == 'nested_method'
        assert method_2.drift['name'] == 'root_method'

        method_1.drift['region_tags'].sort()
        self.assertEqual(
            method_1.drift['region_tags'], ['nested_tag', 'root_tag'])
        self.assertEqual(method_2.drift['region_tags'], ['root_tag'])

    def test_handle_multi_block_region_tags(self):
        source_path = 'test_data/parser/nested_tags/nested_tags.py'

        source_methods = source_parser.get_top_level_methods(source_path)

        source_region_tags = source_parser.get_region_tag_regions(source_path)
        source_parser.add_region_tags_to_methods(
            source_methods, source_region_tags)

        assert len(source_methods) == 3
        method_1 = source_methods[1]
        method_2 = source_methods[2]

        assert hasattr(method_1, 'drift')
        assert hasattr(method_2, 'drift')

        assert method_1.drift['name'] == 'root_method'
        assert method_2.drift['name'] == 'another_root_method'

        self.assertEqual(method_1.drift['region_tags'], ['root_tag'])
        self.assertEqual(method_2.drift['region_tags'], ['root_tag'])