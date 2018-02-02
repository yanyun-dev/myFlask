@main.app_context_processor
def inject_permission():
    return dict(Permission=Permission)