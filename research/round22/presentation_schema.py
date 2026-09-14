"""Shared fail-fast checks for authored presentation metadata, not scientific admission."""
from admission import require


def prose_fields(item, fields, label):
    require(type(item) is dict, label+' must be an object')
    require(all(type(item.get(k)) is str and bool(item[k].strip()) for k in fields),
            label+' requires nonempty prose fields')


def loop_metadata(item, loop):
    prose_fields(item, ['title','novelty_category','prior_work','forward','reverse',
                        'objection','exception'], loop)
    steps=item.get('steps')
    require(type(steps) is list and len(steps)>=3 and
            all(type(s) is str and bool(s.strip()) for s in steps),
            'reviewed derivation must contain at least three nonempty strings: '+loop)
    return item


def future_roadmap(roadmap):
    require(type(roadmap) is dict and roadmap.get('executed') is False,
            'future goals must remain unexecuted')
    goals=roadmap.get('goals')
    require(type(goals) is list and len(goals)==3, 'exactly three future goals required')
    for goal in goals:prose_fields(goal,['id','title','target','missing_premise'],'future goal')
    require(len({g['id'] for g in goals})==3, 'future goal IDs must be distinct')
    return roadmap
