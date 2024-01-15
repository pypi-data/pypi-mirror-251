from typing import Callable
from typing_extensions import Annotated
from yaml import safe_load
from enum import Enum
import textwrap
from jinja2 import PackageLoader, Environment
from pydantic import BaseModel
import typer

app = typer.Typer()


class NoNodes(Exception):
    pass


class NodeKind(str, Enum):
    opportunity = 'opportunity'
    solution = 'solution'
    assumption = 'assumption'


class NodeFocus(str, Enum):
    focussed = 'focussed'
    hidden = 'hidden'
    neutral = 'neutral'


class Node(BaseModel):
    id: str
    desc: str
    parent: str = 'root'
    kind: NodeKind = NodeKind.opportunity
    prio: int = 5
    focus: NodeFocus = NodeFocus.neutral


def is_descendent(node: Node, of: Node, ref: dict[str, Node]) -> bool:
    if node.parent == of.id or node.id == of.id:
        return True
    elif node.parent == 'root':
        return False
    else:
        return is_descendent(ref[node.parent], of=of, ref=ref)


def filter_desc(
    nodes: dict[str, Node], predicate: Callable[[Node], bool]
) -> dict[str, Node]:
    with_pred = list(filter_pred(nodes, predicate).values())
    return {
        n.id: n
        for n in nodes.values()
        if any(is_descendent(n, of=m, ref=nodes) for m in with_pred)
    }


def filter_no_desc(
    nodes: dict[str, Node], predicate: Callable[[Node], bool]
) -> dict[str, Node]:
    with_pred = list(filter_pred(nodes, predicate).values())
    return {
        n.id: n
        for n in nodes.values()
        if not any(is_descendent(n, of=m, ref=nodes) for m in with_pred)
    }


def filter_pred(
    nodes: dict[str, Node], predicate: Callable[[Node], bool]
) -> dict[str, Node]:
    return {n.id: n for n in nodes.values() if predicate(n)}


def is_opportunity(n: Node) -> bool:
    return n.kind == NodeKind.opportunity


def is_solution(n: Node) -> bool:
    return n.kind == NodeKind.solution


def is_assumption(n: Node) -> bool:
    return n.kind == NodeKind.assumption


def has_prior_at_least(prio: int) -> Callable[[Node], bool]:
    def p(n: Node) -> bool:
        return n.prio >= prio

    return p


@app.command()
def main(
    filenames: list[str],
    opportunities: Annotated[bool, typer.Option('--opportunities', '-o')] = False,
    solutions: Annotated[bool, typer.Option('--solutions', '-s')] = False,
    assumptions: Annotated[bool, typer.Option('--assumptions', '-a')] = False,
    priority: Annotated[int, typer.Option('--priority', '-p')] = 5,
):

    predicates = []
    if opportunities:
        predicates.append(is_opportunity)
    if solutions:
        predicates.append(is_solution)
    if assumptions:
        predicates.append(is_assumption)

    nodes = {}
    for filename in filenames:
        with open(filename) as f:
            nodes.update({i: Node(id=i, **vals) for i, vals in safe_load(f).items()})

    if any([n.focus == NodeFocus.focussed for n in nodes.values()]):
        nodes = filter_desc(nodes, lambda n: n.focus == NodeFocus.focussed)
    if any([n.focus == NodeFocus.hidden for n in nodes.values()]):
        nodes = filter_no_desc(nodes, lambda n: n.focus == NodeFocus.hidden)

    nodes = filter_desc(nodes, has_prior_at_least(priority))
    if not nodes:
        raise NoNodes(f'No nodes with priority >= {priority}')
    if predicates:
        nodes = filter_pred(nodes, lambda n: any([p(n) for p in predicates]))
        if not nodes:
            raise NoNodes(f'No nodes with {predicates}')

    font = 'Helvetica,Arial,sans-serif'
    properties = ' '.join(['shape="Mrecord"'])
    styles = {
        NodeKind.opportunity: 'style="filled" fillcolor="#ffeeaa"',
        NodeKind.solution: 'style="filled" fillcolor="#aaffff"',
        NodeKind.assumption: 'styel="filled" fillcolor="#aaffaa"',
    }

    for node in nodes.values():
        node.desc = '<br/>'.join(textwrap.wrap(node.desc, width=40))
        if node.parent not in nodes:
            node.parent = 'root'

    env = Environment(loader=PackageLoader('discovereasy'))

    template = env.get_template('graphs.j2.dot')
    print(template.render(
        nodes=nodes.values(),
        fontspec=font,
        properties=properties,
        styles=styles,
    ))


if __name__ == '__main__':
    app()
