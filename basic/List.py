import random

print("Welcome to HangMan games. Best of luck.👍")
animal_names = [
    "lion", "tiger", "elephant", "giraffe", "panda", "kangaroo", "bear", "wolf", "fox", "deer",
    "monkey", "zebra", "cheetah", "leopard", "rabbit", "horse", "dolphin", "whale", "shark", "penguin"
]

food_names = [
    "pizza", "burger", "pasta", "salad", "sushi", "tacos", "steak", "sandwich", "curry", "soup",
    "rice", "bread", "cheese", "chocolate", "icecream", "pancake", "waffle", "omelette", "fruit", "juice"
]

big_city_names = [
    "new york", "london", "paris", "tokyo", "beijing", "mumbai", "sydney", "moscow", "dubai", "berlin",
    "bangkok", "seoul", "shanghai", "istanbul", "rome", "los angeles", "chicago", "toronto", "madrid", "singapore"
]

big_country_names = [
    "usa", "china", "india", "brazil", "russia", "canada", "australia", "japan", "germany", "france",
    "uk", "italy", "mexico", "spain", "south korea", "indonesia", "turkey", "saudi arabia", "argentina", "nigeria"
]

famous_place_names = [
    "eiffel tower", "great wall", "taj mahal", "statue of liberty", "pyramids", "machu picchu", "colosseum",
    "big ben", "mount everest", "grand canyon", "niagara falls", "louvre museum", "stonehenge", "golden gate",
    "christ the redeemer", "sydney opera house", "burj khalifa", "mount fuji", "victoria falls", "times square"
]

bird_names = [
    "eagle", "parrot", "peacock", "sparrow", "owl", "penguin", "flamingo", "hummingbird", "woodpecker", "crow",
    "swan", "duck", "seagull", "heron", "kingfisher", "hawk", "falcon", "canary", "robin", "pigeon"
]


combined_list = animal_names + food_names + big_city_names + big_country_names + famous_place_names + bird_names
for i in combined_list:
    print(i)