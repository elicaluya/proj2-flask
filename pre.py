"""
Test program for pre-processing schedule
"""
import arrow


base = arrow.utcnow()
current = arrow.utcnow()

def process(raw):
	"""
	Line by line processing of syllabus file.  Each line that needs
	processing is preceded by 'head: ' for some string 'head'.	Lines
	may be continued if they don't contain ':'.	 If # is the first
	non-blank character on a line, it is a comment ad skipped. 
	"""

	field = None
	entry = { }
	cooked = [ ] 
	for line in raw:
		line = line.strip()
		if len(line) == 0 or line[0]=="#" :
			continue
		parts = line.split(':')
		if len(parts) == 1 and field:
			entry[field] = entry[field] + line + " "
			continue
		if len(parts) == 2: 
			field = parts[0]
			content = parts[1]
		else:
			raise ValueError("Trouble with line: '{}'\n".format(line) + 
				"Split into |{}|".format("|".join(parts)))

		if field == "begin":
			try:
				base = arrow.get(content, "MM/DD/YYYY")
				# print("Base date {}".format(base.isoformat()))
			except:
				raise ValueError("Unable to parse date {}".format(content))

		elif field == "week":
			if entry:
				cooked.append(entry)
				entry = { }
			entry['topic'] = ""
			entry['project'] = ""
			entry['week'] = content
			
			week0 = base.replace(weeks=-1)
			week_date = week0.replace(weeks=+int(content))
			entry['week_date'] = week_date.format('MMMM DD, YYYY')
			
			if current > week_date.floor('week') and current < week_date.replace(weeks=+1).floor('week'):
				entry['current'] = "current week"
			
		elif field == 'topic' or field == 'project':
			entry[field] = content
		else:
			raise ValueError("Syntax error in line: {}".format(line))

	if entry:
		cooked.append(entry)

	return cooked
	

def main():
	f = open("data/schedule.txt")
	parsed = process(f)
	print(parsed)

if __name__ == "__main__":
	main()

	
	
			
	
