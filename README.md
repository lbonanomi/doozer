# doozer

> In God we trust, all others we audit

This is an appliance that digests the tables of Windows patch version information on https://learn.microsoft.com/en-us/windows/release-health/windows11-release-information and https://learn.microsoft.com/en-us/windows/release-health/release-information and converts them into a RESTful query endpoint. 

This system graciously [hosted](https://doozer.vercel.app/) by [Vercel](https://vercel.com/) on a hobby plan, please don;t make them regret their generosity.

## Example output

https://doozer.vercel.app/latest/19044:
```
{
  "latest": {
    "authority": "https://learn.microsoft.com/en-us/windows/release-health/release-information",
    "kb": "https://support.microsoft.com/help/5039211",
    "patch_number": "4529"
  },
  "previous": {
    "authority": "https://learn.microsoft.com/en-us/windows/release-health/release-information",
    "kb": "https://support.microsoft.com/help/5036892",
    "patch_number": "4291"
  },
  "release": "19044",
  "stable": {
    "authority": "https://learn.microsoft.com/en-us/windows/release-health/release-information",
    "kb": "https://support.microsoft.com/help/5037768",
    "patch_number": "4412"
  }
}
```

## Bootstrapping the postgres database

**TODO:** automate this.

`create table windows(service_option VARCHAR(50), availability_date DATE, release VARCHAR(50), patch VARCHAR(50), authority VARCHAR(255) );`

