from googlesearch import search

class WebSurfer:
    @staticmethod
    def google_search_keywords(search_query: str):
        response = search(search_query, num=10, stop=10)
        return response

if __name__ == '__main__':
    WebSurfer.google_search_keywords('car')
