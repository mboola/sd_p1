import redis

# Connect to Redis
server = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

insult_list = "insult_list"

insults = [
	"papanatas", "bobo", "estupido", "bobete",   "nincompoop", "buffoon", "dimwit", "clod", "doofus", "numbskull", "dullard", "simpleton", "twit", "loon",
	"blockhead", "nitwit", "goofball", "bonehead", "blunderer", "muttonhead", "dunderhead", "chowderhead", "fool",
	"airhead", "birdbrain", "dunce", "lunkhead", "meathead", "dingbat", "twaddle", "clown", "bumbler", "nit",
	"lamebrain", "moron", "peabrain", "wazzock", "drongo", "spanner", "mug", "goblin", "wally", "twerp",
	"prat", "numpty", "dope", "tool", "oaf", "muppet", "bozo", "git", "pillock", "klutz",
	"turkey", "nerfherder", "twonk", "schmuck", "pipsqueak", "grump", "rascal", "scallywag", "scamp", "wretch",
	"rapscallion", "cad", "blaggard", "charlatan", "twaddlehead", "snollygoster", "blowhard", "loudmouth", "scoundrel", "knave",
	"toerag", "scuzzball", "nutter", "dingus", "ninny", "crank", "cur", "yokel", "rube", "goon",
	"hooligan", "lackwit", "dodo", "ignoramus", "zany", "bungler", "gomer", "slugabed", "leech", "drip",
	"flake", "loonball", "doink", "snob", "weasel", "cringer", "poser", "cheeser", "slug", "grouch"
]

for i in range(len(insults)):
	server.rpush(insult_list, insults[i])
