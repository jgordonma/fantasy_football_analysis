def clean_file(filename):
    fi = open(filename, 'rb')
    data = fi.read()
    fi.close()
    fo = open(filename, 'wb')
    fo.write(data.replace('\x00', ''))
    fo.close()

if __name__ == "__main__":
    # Replace these filenames with the actual paths to your files
    tab_separated_file = "player_stats.tsv"
    csv_file = "draftresults.csv"
    clean_file(tab_separated_file)
    clean_file(csv_file)