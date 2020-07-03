from .cli import main
import os, sys

if __name__ == '__main__':
	
	# Rewrite sys.argv[0] so our help prompts display a pretty base command
	sys.argv[0] = 'gen-invoice'
	main()
