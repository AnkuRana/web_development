import requests

headers = {
	"X-RapidAPI-Key": "get_your_own_key",
	"X-RapidAPI-Host": "online-movie-database.p.rapidapi.com"
}

def get_movie(movie_name, headers):
    url = "https://online-movie-database.p.rapidapi.com/auto-complete"
    querystring = {
        "q":movie_name
        }
    response = requests.request("GET", url, headers=headers, params=querystring)
    response.raise_for_status()
    movie_list = response.json()["d"]
    # for movie in movie_list:
    #     print(f"Movie:{movie['l']}, Movie_id: {movie['id']}, Movie_year: {movie['y']}, type: {movie['qid']}")
    return movie_list

def get_movie_details(movie_id, headers):
    url = "https://online-movie-database.p.rapidapi.com/title/get-overview-details"
    querystring = {
        "tconst":movie_id
        }
    response = requests.request("GET", url, headers=headers, params=querystring)
    response.raise_for_status()
    movie_details = response.json()
    delimiter = "-"
    top_rank = "Not Ranked"
    plotOutline = ""
    plotSummary =""
    author = ""
    movie_genre = delimiter.join(movie_details["genres"])
    if "topRank" in movie_details["ratings"].keys():
        top_rank = movie_details["ratings"]["topRank"]
    if "plotOutline" in movie_details.keys():
        plotOutline = movie_details["plotOutline"]["text"]
    if "plotSummary" in movie_details.keys():
        plotSummary = movie_details["plotSummary"]["text"]
        author = movie_details["plotSummary"]["author"]

    movie_req_info = {
        "image": movie_details["title"]["image"]["url"],
        "type": movie_details["title"]["titleType"],
        "title": movie_details["title"]["title"],
        "year": movie_details["title"]["year"],
        "rating": movie_details["ratings"]["rating"],
        "toprank": top_rank,
        "genres_list": movie_genre,
        "plot_outline": plotOutline,
        "plot_summary": plotSummary,
        "author": author
    }
    return movie_req_info
