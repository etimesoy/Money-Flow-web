def get_nav_links(overview: bool = False,
                  limits: bool = False,
                  reports: bool = False) -> dict:
    return {
        "overview": "active" if overview else "",
        "limits": "active" if limits else "",
        "reports": "active" if reports else ""
    }
