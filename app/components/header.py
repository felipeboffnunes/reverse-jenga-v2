from dash import html


def create_menu_links(menu_options):
    """
    Creates a list of hyperlink components for menu options.

    Parameters:
    menu_options (list of tuples): A list of tuples, each containing the display text and URL for a menu option.

    Returns:
    list: A list of dash_html_components.A elements representing the menu links.
    """
    return [html.A(option_text, className='menu-option', style={'margin': '0 10px'}) for option_text in menu_options]
