import csv
import json

states = {}
cities = []

with open("uscities.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)

    for row in reader:
        state_code = row["state_id"]
        state_name = row["state_name"]

        if state_code not in states:
            states[state_code] = {
                "name": state_name,
                "code": state_code,
                "country_code": "USA"
            }

        cities.append({
            "name": row["city"],
            "city_ascii": row["city_ascii"],
            "state_code": row["state_id"],
            "state_name": row["state_name"],
            "county_fips": row["county_fips"],
            "county_name": row["county_name"],
            "lat": float(row["lat"]) if row["lat"] else None,
            "lng": float(row["lng"]) if row["lng"] else None,
            "population": int(float(row["population"])) if row["population"] else None,
            "density": float(row["density"]) if row["density"] else None,
            "source": row["source"],
            "military": row["military"].strip().lower() == "true",
            "incorporated": row["incorporated"].strip().lower() == "true",
            "timezone": row["timezone"],
            "ranking": int(row["ranking"]) if row["ranking"] else None,
            "zips": row["zips"].split() if row["zips"] else [],
            "id": row["id"]
        })

geo_data = {
    "states": list(states.values()),
    "cities": cities
}

with open("full_geo.json", "w", encoding="utf-8") as f:
    json.dump(geo_data, f, indent=2)

print("Done! Created full_geo.json with expanded city fields.")
print(f"States: {len(geo_data['states'])}")
print(f"Cities: {len(geo_data['cities'])}")