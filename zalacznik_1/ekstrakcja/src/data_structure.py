from dataclasses import dataclass

# Klasa bazowa reprezentująca post
@dataclass
class Post:
    shortcode: str
    typename: str
    creation_timestamp: int
    likes: int
    comments: int
    captions: str
    comments_disabled: bool

# Klasa reprezentująca post wideo
@dataclass
class VideoPost(Post):
    video_view_count: int
    video_url: str

# Klasa reprezentująca post ze zdjęciem
@dataclass
class ImagePost(Post):
    image_url: str

# Klasa reprezentująca post typu karuzela (sidecar)
@dataclass
class SidecarPost(Post):
    sidecar_url_list: list[str]

# Funkcja parsująca odpowiedź z Instagrama i zwracająca listę obiektów postów
def parse_response(data: dict):
    return_data = []
    edges_list = data['data']['user']['edge_owner_to_timeline_media']['edges']
    for e in edges_list:
        shortcode = e['node']['shortcode']
        typename = e['node']["__typename"]
        creation_timestamp  = e['node']["taken_at_timestamp"]
        likes = e['node']['edge_media_preview_like']['count']
        comments = e['node']['edge_media_to_comment']['count']
        try:
            captions = e['node']['edge_media_to_caption']['edges'][0]['node']['text']
        except Exception as err:
            captions = ""
            print(f'error loading captions: {err}')
        comments_disabled = e['node']['comments_disabled']
        # Tworzenie obiektu w zależności od typu posta
        if typename == "GraphImage":
            image_url = e['node']['display_url']
            post = ImagePost(shortcode, typename, creation_timestamp, likes, comments, captions, comments_disabled, image_url)
        elif typename == "GraphVideo":
            video_view_count = e['node']['video_view_count']
            video_url = e['node']['video_url']
            post = VideoPost(shortcode, typename, creation_timestamp, likes, comments, captions, comments_disabled, video_view_count, video_url)
        elif typename == "GraphSidecar":
            sidecar_url_list = [i['node']['display_url'] for i in e['node']['edge_sidecar_to_children']['edges']]
            post = SidecarPost(shortcode, typename, creation_timestamp, likes, comments, captions, comments_disabled, sidecar_url_list)
        else:
            continue
        return_data.append(post)
    return return_data

# Funkcja wyciągająca cursor do kolejnej strony postów
def extract_cursor(data: dict):
    try:
        return data['data']['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']
    except Exception as err:
        print(f'error loading response as response: {err}')
        return ""
