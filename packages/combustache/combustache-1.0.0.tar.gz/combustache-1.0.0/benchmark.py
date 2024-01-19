import cProfile
import json
import pstats
from typing import Callable

import chevron
import combustache

template = """
<%firstName%> <%lastName%> <%>id%> is an <%occupation%>
<%= {{ }} =%>
Affirmatives:
{{#affirmatives}}
  {{>affirmative}}

{{/affirmatives}}
 0. {{affirmatives.0.status}}
 3. {{affirmatives.3.status}}
-1. {{affirmatives.-1.status}}
-2. {{affirmatives.-2.status}}
{{! is this a comment? }}
Condition: {{>cond}}
"""
data_str = """
{
  "id": 70,
  "firstName": "Sliver",
  "lastName": "of Straw",
  "occupation": "Iterator",
  "affirmatives": [
    {"name": "First", "status": true},
    {"name": "Second", "status": true},
    {"name": "Third", "status": true},
    {"name": "Always False", "status": false}
  ],
  "condition": "Dead"
}
"""
data = json.loads(data_str)


def benchmark(
    func: Callable,
    template: str,
    data: dict,
    partials: dict | None = None,
    num: int = 200_000,
) -> pstats.Stats:
    with cProfile.Profile() as pr:
        for _ in range(num):
            func(template, data)
    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    return stats


combustache_stats = benchmark(combustache.render, template, data)
combustache_stats.dump_stats('combustache_stats.prof')
chevron_stats = benchmark(chevron.render, template, data)
chevron_stats.dump_stats('chevron_stats.prof')
