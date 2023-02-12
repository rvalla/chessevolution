from PIL import Image as im

class PositionImage():
	"The class to convert a fen chess position in an image..."

	fen_pieces = {"P": [0,0], "N": [0,1], "B": [0,2], "R": [0,3], "Q": [0,4], "K": [0,5],
				"p": [1,0], "n": [1,1], "b": [1,2], "r": [1,3], "q": [1,4], "k": [1,5]}

	def __init__(self, size, sq_size):
		self.sq_size = sq_size
		self.size = size
		self.pieces = self.load_pieces()

	def position_to_image(self, fen, output):
		rows = fen.split(" ")[0].split("/")
		image = im.open("img/boardG.png").resize((self.size, self.size))
		x = 0
		y = 0
		for r in range(8):
			x = 0
			for c in rows[r]:
				try: 
					x += int(c)
				except:
					coordinates = self.get_piece_index(c)
					piece = self.pieces[coordinates[0]][coordinates[1]]
					image.paste(piece, (x * self.sq_size, y * self.sq_size), mask=piece)
					x += 1
			y += 1
		image.save(output, "png", quality=85, optimize=True)

	def get_piece_index(self, p):
		return self.fen_pieces[p]

	def load_pieces(self):
		print("Loading pieces...", end="\r")
		pieces = []
		white = []
		white.append(im.open("img/wP.png").resize((self.sq_size, self.sq_size)))
		white.append(im.open("img/wN.png").resize((self.sq_size, self.sq_size)))
		white.append(im.open("img/wB.png").resize((self.sq_size, self.sq_size)))
		white.append(im.open("img/wR.png").resize((self.sq_size, self.sq_size)))
		white.append(im.open("img/wQ.png").resize((self.sq_size, self.sq_size)))
		white.append(im.open("img/wK.png").resize((self.sq_size, self.sq_size)))
		black = []
		black.append(im.open("img/bP.png").resize((self.sq_size, self.sq_size)))
		black.append(im.open("img/bN.png").resize((self.sq_size, self.sq_size)))
		black.append(im.open("img/bB.png").resize((self.sq_size, self.sq_size)))
		black.append(im.open("img/bR.png").resize((self.sq_size, self.sq_size)))
		black.append(im.open("img/bQ.png").resize((self.sq_size, self.sq_size)))
		black.append(im.open("img/bK.png").resize((self.sq_size, self.sq_size)))
		pieces.append(white)
		pieces.append(black)
		return pieces

	def __str__(self):
		return "Hi, I am an the class to transform a fen chess position on an image..."
