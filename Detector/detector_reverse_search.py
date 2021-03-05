def image_search(photo: bytes) -> str:
    """performing Google reverse image search and returning the name of the captured object"""
    from bs4 import BeautifulSoup
    import requests

    url = "https://www.google.com/searchbyimage/upload"
    file = {'encoded_image': (None, photo, "multipart/form-data")}
    headers = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/87.0.4280.88 Safari/537.36'}
    try:
        # post request with a binary image file
        response = requests.post(url=url, files=file, allow_redirects=False)
        response.raise_for_status()  # raise Exception if request is unsuccessful
        # get the search results page
        photo_url = response.headers["Location"]
        response1 = requests.get(photo_url, headers=headers, params={"hl": "EN"})
        response1.raise_for_status()  # raise Exception if request is unsuccessful
        all_results = BeautifulSoup(response1.text, "html.parser")
        # fetch the result word(s) from the search line (next to image)
        result = all_results.find("a", {"class": "fKDtNb"}).text
        if result:
            return f"There is probably {result} in front of you."
        else:
            return "I could not find anything."
    except Exception:
        return "I could not perform an image analysis."
