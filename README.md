# doozer

> I remember the dark time before Patch Tuesdays


This is an appliance that digests the tables of Windows patch version information on https://learn.microsoft.com/en-us/windows/release-health/windows11-release-information and https://learn.microsoft.com/en-us/windows/release-health/release-information and converts them into a RESTful query endpoint. 

This system graciously [hosted](https://doozer.vercel.app/) by [Vercel](https://vercel.com/) on a microscopic plan, _please_ don't make them regret their generosity.


## Response structure

**Queries will always return 3 values:**

`latest`: The latest patch for the product number  
`stable`: The next-latest patch for the product number for shops using a latest-but-one standard  
`previous`: The second-latest patch for the product number for shops that consider this the oldest-acceptable version  

**Each value features:**

`authority`: Which [https://learn.microsoft.com](https://learn.microsoft.com) URL mentions this patch  
`kb`: The [support.microsoft.com](https://support.microsoft.com) URL detailing that individual patch  
`patch_number`: The patch number  

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
