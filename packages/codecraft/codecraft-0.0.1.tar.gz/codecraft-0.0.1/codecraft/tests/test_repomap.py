from codecraft.repomap import parse_code, get_repomap


def test_parse_code_exception_handling():
    invalid_code = None  # None is not a valid input and should trigger an exception
    result = parse_code(invalid_code)
    assert result == {'class': {}, 'function': []}  # Expecting the default elements structure


def test_render_repo_map_with_files_and_names():
    # Test the render_repo_map function with files_and_names set to True
    files, names = get_repomap(files_and_names=True)
    assert isinstance(files, list)
    assert isinstance(names, list)
    assert all(isinstance(file, str) for file in files)
    assert all(isinstance(name, str) for name in names)

