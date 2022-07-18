from re import sub

class RenderGames:
    """
    Render HTML for further display via web server.
    Sorry, no Flask, need to keep this running as fast as possible.
    """
    def __init__(self):
        pass

    def render_list(
            self,
            data_list: list,
            core_class="data_block",
            line_class="data_line",
            cell_class="data_cell"
        ) -> str:
        """
        Render data in convenient HTML form.
        """
        return_html = f"<div class='{core_class}'>\n"
        for l in data_list:
            return_html += f"<div class='{line_class}'>\n"
            for c in l:
                return_html += f"<div class='{cell_class}'>{c}</div>\n"
            return_html += "</div>"
        return_html += "</div>"
        return return_html

    def read_resource(self, res_path: str) -> str:
        """
        Read resource from file and return string.
        """
        with open(res_path, 'r') as file:
            data = file.read()
        return data

    def merge_template(
            self,
            html_path: str,
            css_path: str,
            title: str="",
        ) -> str:
        """
        Merge generated HTML with template and css.
        """
        html = self.read_resource(html_path)
        if len(title) > 0:
            html = sub('@@title@@', title, html)
        css = self.read_resource(css_path)
        return sub('@@style@@', css, html)


def main():
    pass

if __name__ == '__main__':
    main()

