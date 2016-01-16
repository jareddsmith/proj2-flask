"""
Test program for pre-processing schedule
"""
import arrow

base = arrow.now()

def process(raw):
    """
    Line by line processing of syllabus file.  Each line that needs
    processing is preceded by 'head: ' for some string 'head'.  Lines
    may be continued if they don't contain ':'.  
    """
    field = None
    entry = { }
    cooked = [ ] 
    for line in raw:
        line = line.rstrip()
        if len(line) == 0:
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
            	#Creates an arrow object from the begin date
            	
                base = arrow.get(content)
            except:
                raise ValueError("Unable to parse date {}".format(content))

        elif field == "week":
            if entry:
                cooked.append(entry)
                entry = { }
            entry['topic'] = ""
            entry['project'] = ""
            entry['week'] = content
            
            counted_days = count_days(content)
            week_start = base.replace(days=+counted_days)
            entry['date'] = arrow.Arrow.isoformat(week_start)

        elif field == 'topic' or field == 'project':
            entry[field] = content

        else:
            raise ValueError("Syntax error in line: {}".format(line))

    if entry:
        cooked.append(entry)

    return cooked
    
def count_days(week):
	"""
	Calculates the number of days that have passed since the beginning date.
	"""
	
	return (int(week)- 1)*7

def main():
    f = open("static/schedule.txt")
    parsed = process(f)
    print(parsed)

if __name__ == "__main__":
    main()

    
    
            
    
