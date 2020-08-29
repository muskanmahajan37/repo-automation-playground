import json

from . import polyglot_parser, yaml_utils


def analyze_json(repo_json, root_dir):
    json_methods = []
    with open(repo_json, 'r') as file:
        json_content = '\n'.join(file.readlines())
        json_methods = json.loads(json_content)

    source_filepaths = set([m['source_path'] for m in json_methods])

    grep_tags = set()
    ignored_tags = set()

    for source_file in source_filepaths:
        (region_tags, ignored_tag_names) = \
            polyglot_parser.get_region_tag_regions(source_file)

        grep_tags = grep_tags.union(set([t[0] for t in region_tags]))
        ignored_tags = ignored_tags.union(set(ignored_tag_names))

        file_methods = [m for m in json_methods
                        if m['source_path'] == source_file]

        polyglot_parser.add_region_tags_to_methods(
            file_methods, region_tags)

    source_methods = [m for m in json_methods if m['region_tags']]

    # Dedupe source methods
    source_method_keys = set()
    source_methods_deduped = []
    for m in source_methods:
        key = ','.join(m['region_tags'])
        if key not in source_method_keys:
            source_methods_deduped.append(m)
            source_method_keys.add(key)

    source_methods = source_methods_deduped

    # Convert test_methods values to tuples
    for m in source_methods:
        m['test_methods'] = [tuple(x) for x in m['test_methods']]

    polyglot_parser.add_children_drift_data(source_methods)

    yaml_utils.add_yaml_data_to_source_methods(source_methods, root_dir)

    source_tags = set()
    for m in source_methods:
        source_tags = source_tags.union(set(m['region_tags']))

    # Remove automatically ignored region tags from region tag lists
    grep_tags = [x for x in grep_tags if x not in ignored_tags]
    source_tags = [x for x in source_tags if x not in ignored_tags]

    # Add manually ignored (via yaml) tags to ignored tags list
    #   These should *not* overlap w/ source_tags, but we
    #   check that in validate_yaml_syntax  - *not here!*
    ignored_tags = ignored_tags.union(
        yaml_utils.get_untested_region_tags(root_dir))

    return (grep_tags, source_tags, list(ignored_tags), source_methods)