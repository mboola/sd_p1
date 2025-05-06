import time
import xmlrpc.client
from concurrent.futures import ThreadPoolExecutor

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

n_insults = len(insults)
TOTAL_REQUESTS = 5000
MAX_THREADS = 4  # Tune based on system/network capabilities

# Get server proxies
name_server = xmlrpc.client.ServerProxy('http://localhost:8000')
insult_service_workers_uri = name_server.get_insult_workers()
n_workers = len(insult_service_workers_uri)

# Function to send a single request
def send_insult(i):
	try:
		insult_service = xmlrpc.client.ServerProxy(insult_service_workers_uri[i % n_workers])
		insult_service.add_insult(insults[i % n_insults])
		return "sent"
	except Exception as e:
		print(f"Error: {e}")
		return "wtf"

# Start timing
start_time = time.time()

# Launch in parallel
with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
	futures = [executor.submit(send_insult, i) for i in range(TOTAL_REQUESTS)]

	# Wait for the results and collect them
	results = [future.result() for future in futures]

# Done
print(f"Total time: {time.time() - start_time:.2f} seconds")
