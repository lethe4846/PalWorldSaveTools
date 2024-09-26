import csv

def parse_logfile(log_path):
    with open(log_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    guild_data = []
    current_guild = {}
    base_keys = set()
    total_bases = 0  # Counter for total bases
    level_55_count = 0  # Counter for Level: 55 occurrences

    for line in lines:
        if line.startswith('Guild:'):
            if current_guild:
                guild_data.append(current_guild)
                current_guild = {}
            guild_info = line.strip().split('|')
            current_guild['Guild'] = guild_info[0].split(': ')[1].strip()
            current_guild['Guild Leader'] = guild_info[1].split(': ')[1].strip()

        if line.startswith('Base ') and line.split(':')[0].strip() in ['Base 1', 'Base 2', 'Base 3', 'Base 4']:  # Only count specific base entries
            base_info = line.strip().split(':')
            base_key = base_info[0].strip()
            current_guild[base_key] = base_info[1].strip()
            base_keys.add(base_key)
            total_bases += 1  # Increment base counter only for specific bases

        if "Level: 55" in line:
            level_55_count += 1  # Increment the count for Level: 55

    if current_guild:
        guild_data.append(current_guild)

    print(f'Total bases found: {total_bases}')  # Print total bases
    print(f'Total guilds processed: {len(guild_data)}')  # Print total guilds
    print(f'Total Level 55 occurrences: {level_55_count}')  # Print total Level 55 occurrences
    return guild_data, sorted(base_keys)

def write_csv(guild_data, base_keys, output_file):
    fieldnames = ['Guild', 'Guild Leader'] + base_keys
    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for guild in guild_data:
            row = {field: guild.get(field, '') for field in fieldnames}
            writer.writerow(row)

if __name__ == "__main__":
    log_file = 'fix_save.log'
    guild_data, base_keys = parse_logfile(log_file)
    write_csv(guild_data, base_keys, 'bases.csv')
