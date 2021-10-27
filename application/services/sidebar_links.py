def get_nav_links(overview: bool = False,
                  limits: bool = False,
                  settings: bool = False,
                  categories: bool = False) -> dict:
    return {
        "overview": "active" if overview else "",
        "limits": "active" if limits else "",
        "settings": "active" if settings else "",
        "categories": "active" if categories else "",
    }
