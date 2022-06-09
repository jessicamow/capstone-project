STREAMING_SERVICES = {'Netflix': 8, 
                    'Amazon Prime Video': 9, 
                    'Disney Plus': 337, 
                    'Apple iTunes': 2, 
                    'Google Play Movies': 3,  
                    'fuboTV': 257, 
                    'Hulu': 15, 
                    'Paramount Plus': 531, 
                    'Netflix Kids': 175, 
                    'HBO Max': 384, 
                    'Crunchyroll': 283, 
                    'Peacock': 386, 
                    'Acorn TV': 87, 
                    'Peacock Premium': 387, 
                    'Apple TV Plus': 350, 
                    'Amazon Video': 10, 
                    'YouTube': 192, 
                    'Discovery+ Amazon Channel': 584, 
                    'Showtime Amazon Channel': 203, 
                    'AMC+ Amazon Channel': 528, 
                    'HBO Now': 27, 
                    'The Roku Channel': 207, 
                    'Rakuten Viki': 344, 
                    'YouTube Premium': 188,
                    'Starz': 43, 
                    'PBS': 209, 
                    'CBS': 78, 
                    'FXNow': 123,
                    'Redbox': 279, 
                    'ABC': 148, 
                    'DIRECTV': 358, 
                    'AMC': 80, 
                    'NBC': 79, 
                    'History': 155, 
                    'Syfy': 215, 
                    'Lifetime': 157, 
                    'Hallmark Movies': 281, 
                    'PBS Kids Amazon Channel': 293, 
                    'MTV': 453, 
                    'Cartoon Network': 317, 
                    'Adult Swim': 318, 
                    'USA Network': 322, 
                    'Fox': 328, 
                    'TNT': 363, 
                    'Food Network': 366, 
                    'BBC America': 397, 
                    'Science Channel': 411, 
                    'Animal Planet': 399, 
                    'Discovery Life': 404, 
                    'Discovery': 403, 
                    'Cooking Channel': 400, 
                    'Travel Channel': 413, 
                    'Paramount Network': 418, 
                    'TBS': 506, 
                    'OXYGEN': 487, 
                    'tru TV': 507
                    }

GENRES =        {'Action': 28, 
                'Adventure': 12, 
                'Animation': 16, 
                'Comedy': 35, 
                'Crime': 80, 
                'Documentary': 99, 
                'Drama': 18, 
                'Family': 10751, 
                'Fantasy': 14, 
                'History': 36, 
                'Horror': 27, 
                'Kids': 10762, 
                'Music': 10402, 
                'Mystery': 9648, 
                'News': 10763, 
                'Reality': 10764, 
                'Romance': 10749, 
                'Science Fiction': 878, 
                'Soap': 10766, 
                'Talk': 10767, 
                'TV Movie': 10770, 
                'Thriller': 53, 
                'War': 10752, 
                'Western': 37
                }


TV_GENRES = {'Action & Adventure': 10759, 

            'Kids': 10762, 

            'News': 10763, 
            'Reality': 10764, 

            'Sci-Fi & Fantasy': 10765, 

            'Soap': 10766, 
            'Talk': 10767, 
            'War & Politics': 10768
            }



MOVIE_GENRES = {'Action': 28, 
                'Adventure': 12, 

                'Fantasy': 14, 
                'History': 36, 
                'Horror': 27, 

                'Music': 10402, 

                'Romance': 10749, 
                'Science Fiction': 878, 
                'TV Movie': 10770, 
                'Thriller': 53, 
                'War': 10752
                }

def filter_genre(media_type, genre_key):
    only_in_tv = ['Kids', 'News', 'Reality', 'Soap', 'Talk']
    only_in_movies = ['History', 'Horror', 'Music', 'Romance', 'TV Movie', 'Thriller']
    if media_type == "tv":
        if genre_key == "Action" or genre_key == "Adventure":
            return 10759
        if genre_key == "Science Fiction" or genre_key == "Fantasy":
            return 10765
        if genre_key == "War":
            return 10768
        if genre_key in only_in_movies:
            return None
            # return f"Sorry, there are no correlated TV shows with genre {genre_key}. Please try searching again."
        else:
            return GENRES.get(genre_key, None)
    if media_type == "movie":
        if genre_key in only_in_tv:
            return None 
            # return f"Sorry, there are no correlated movies with genre {genre_key}. Please try searching again."
        else:
            return GENRES.get(genre_key, None)


def get_genre_data(genre_name):
    if genre_name == 'Action & Adventure':
        return ['Action', 'Adventure']
    elif genre_name == 'Sci-Fi & Fantasy':
        return ['Science Fiction', 'Fantasy']
    elif genre_name == 'War & Politics':
        return ['War']
    else: 
        return [genre_name]


# STREAMING_SERVICES = {'Netflix': 8, 'Amazon Prime Video': 9, 'Disney Plus': 337, 'Apple iTunes': 2, 'Google Play Movies': 3, 'Sun Nxt': 309, 'fuboTV': 257, 'Classix': 445, 'Hulu': 15, 'Rooster Teeth': 485, 'Paramount Plus': 531, 'Netflix Kids': 175, 'HBO Max': 384, 'Crunchyroll': 283, 'Peacock': 386, 'Cultpix': 692, 'Acorn TV': 87, 'Peacock Premium': 387, 'Apple TV Plus': 350, 'Amazon Video': 10, 'FilmBox+': 701, 'VIX ': 457, 'YouTube': 192, 'Curiosity Stream': 190, 'Kocowa': 464, 'Funimation Now': 269, 'Starz Play Amazon Channel': 194, 'WOW Presents Plus': 546, 'Paramount+ Amazon Channel': 582, 'Magellan TV': 551, 'EPIX Amazon Channel': 583, 'BroadwayHD': 554, 'Discovery+ Amazon Channel': 584, 'Showtime Amazon Channel': 203, 'Dekkoo': 444, 'AMC+ Amazon Channel': 528, 'HBO Now': 27, 'Hoichoi': 315, 'The Roku Channel': 207, 'BritBox': 151, 'Rakuten Viki': 344, 'Showtime Roku Premium Channel': 632, 'Pluto TV': 300, 'iQIYI': 581, 'Paramount+ Roku Premium Channel': 633, 'Starz Roku Premium Channel': 634, 'AMC+ Roku Premium Channel': 635, 'Epix Roku Premium Channel': 636, 'HBO Max Free': 616, 'YouTube Premium': 188, 'Hoopla': 212, 'The CW': 83, 'CW Seed': 206, 'Vudu': 7, 'VUDU Free': 332, 'Starz': 43, 'Showtime': 37, 'PBS': 209, 'Pantaflix': 177, 'CBS': 78, 'FXNow': 123, 'Tubi TV': 73, 'Kanopy': 191, 'Comedy Central': 243, 'Microsoft Store': 68, 'Redbox': 279, 'Max Go': 139, 'ABC': 148, 'DIRECTV': 358, 'Crackle': 12, 'AMC': 80, 'NBC': 79, 'Epix': 34, 'Freeform': 211, 'History': 155, 'Syfy': 215, 'A&E': 156, 'Lifetime': 157, 'Shudder': 99, 'Sundance Now': 143, 'Popcornflix': 241, 'Pantaya': 247, 'Boomerang': 248, 'Urban Movie Channel': 251, 'Dove Channel': 254, 'Yupp TV': 255, 'Eros Now': 218, 'Magnolia Selects': 259, 'WWE Network': 260, 'MyOutdoorTV': 264, 'Nickhits Amazon Channel': 261, 'Noggin Amazon Channel': 262, 'Hopster TV': 267, 'Laugh Out Loud': 275, 'Smithsonian Channel': 276, 'Pure Flix': 278, 'Hallmark Movies': 281, 'PBS Kids Amazon Channel': 293, 'Boomerang Amazon Channel': 288, 'Cinemax Amazon Channel': 289, 'Pantaya Amazon Channel': 292, 'Hallmark Movies Now Amazon Channel': 290, 'PBS Masterpiece Amazon Channel': 294, 'Viewster Amazon Channel': 295, 'MZ Choice Amazon Channel': 291, 'Sling TV': 299, 'HiDive': 430, 'Topic': 454, 'MTV': 453, 'Retrocrush': 446, 'Shout! Factory TV': 439, 'Chai Flicks': 438, 'Mhz Choice': 427, 'Vice TV ': 458, 'Shudder Amazon Channel': 204, 'AcornTV Amazon Channel': 196, 'BritBox Amazon Channel': 197, 'Fandor Amazon Channel': 199, 'Screambox Amazon Channel': 202, 'Sundance Now Amazon Channel': 205, 'Cartoon Network': 317, 'Adult Swim': 318, 'USA Network': 322, 'Fox': 328, 'FlixFling': 331, 'Bet+ Amazon Channel': 343, 'Darkmatter TV': 355, 'Bravo TV': 365, 'TNT': 363, 'Food Network': 366, 'BBC America': 397, 'IndieFlix': 368, 'AHCTV': 398, 'TLC': 412, 'HGTV': 406, 'DIY Network': 405, 'Investigation Discovery': 408, 'Science Channel': 411, 'Destination America': 402, 'Animal Planet': 399, 'Discovery Life': 404, 'Discovery': 403, 'Motor Trend': 410, 'Cooking Channel': 400, 'Travel Channel': 413, 'Paramount Network': 418, 'Here TV': 417, 'TV Land': 419, 'Logo TV': 420, 'VH1': 422, 'DreamWorksTV Amazon Channel': 263, 'TBS': 506, 'AsianCrush': 514, 'FILMRISE': 471, 'Revry': 473, 'Spectrum On Demand': 486, 'OXYGEN': 487, 'VRV': 504, 'tru TV': 507, 'DisneyNOW': 508, 'WeTV': 509, 'Discovery Plus': 520, 'ARROW': 529, 'Plex': 538, 'The Oprah Winfrey Network': 555, 'British Pathé TV': 571, 'Freevee Amazon Channel': 613, 'Netflix Free': 459, 'CBS All Access Amazon Channel': 198, 'Mubi': 11, 'GuideDoc': 100, 'Public Domain Movies': 638, 'Argo': 534, 'Eventive': 677, 'Spamflix': 521, 'DOCSVILLE': 475, 'Filmzie': 559, 'True Story': 567, 'DocAlliance Films': 569, 'KoreaOnDemand': 575, 'YouTube Free': 235, 'Criterion Channel': 258, 'ShortsTV Amazon Channel': 688, 'Fandor': 25, 'Screambox': 185, 'realeyz': 14, 'History Vault': 268, 'Lifetime Movie Club': 284, 'Night Flight Plus': 455, 'OVID': 433, 'The Film Detective': 470, 'Mubi Amazon Channel': 201, 'AMC on Demand': 352, 'TCM': 361, 'Flix Premiere': 432, 'Hi-YAH': 503, 'Alamo on Demand': 547, 'MovieSaints': 562, 'Dogwoof On Demand': 536, 'Film Movement Plus': 579, 'Metrograph': 585, 'Curia': 617, 'Kino Now': 640, 'Cinessance': 694}
