from derpibooru import sort

def test_sorting_methods():
    sorting_methods = {
        "created_at",
        "updated_at",
        "first_seen_at",
        "aspect_ratio",
        "faves",
        "upvotes",
        "downvotes",
        "score",
        "wilson_score",
        "relevance",
        "width",
        "height",
        "comments",
        "tag_count",
        "random",
    }

    methods = sort.__dict__

    assert len(sorting_methods) == len(methods)
    assert sorting_methods == sort.methods

    for key, value in methods.items():
        assert key == value.upper()
