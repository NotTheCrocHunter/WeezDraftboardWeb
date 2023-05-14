from sleeper_wrapper import Stats

stats = Stats()

for x in range(2008, 2023):
    print(f'Grabbing {x}')
    stats.season = x
    stats.week_start = 1
    stats.week_stop = 18
    stats.get_stats()
print(dir(stats))