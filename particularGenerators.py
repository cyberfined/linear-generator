import genericGenerators 
from utils import scalarType

def funcName(t, n):
    return "{}_{}".format(t,n)

def funcProto(vec, scalar, name, **kwargs):
    pf = funcs[name]
    data = {
            "func": funcName(vec, name),
            "type": vec,
            "scalar": scalar,
            "rscalar": scalarType(scalar)
    }
    for k,v in kwargs.items(): data[k] = v
    proto = pf[:pf.find(")") + 1] + ";"
    return proto.format(**data)

def funcBody(vec, scalar, name, size, **kwargs):
    data = {
            "func": funcName(vec, name),
            "type": vec,
            "size": size,
            "scalar": scalar,
            "rscalar": scalarType(scalar)
    }
    for f,v in genericGenerators.getFuncs().items(): data[f] = genericGenerators.funcName(scalar, f)
    for k,v in kwargs.items(): data[k] = v
    return funcs[name].format(**data)

zero = """\
{type} {func}() {{
    {type} out;
    {zero}(({scalar}*)&out, {size});
    return out;
}}"""

identity = """\
{type} {func}() {{
    {type} out;
    {identity}(({scalar}*)&out, {rows});
    return out;
}}"""

transpose = """\
{type} {func}({type} m) {{
    {type} out;
    {transpose}(({scalar}*)&out, {rows});
    return out;
}}"""

mmult = """\
{rtype} {func}({type} m, {rtype} a) {{
    {rtype} out;
    {mmult}(({scalar}*)&m, ({scalar}*)&a, ({scalar}*)&out, {rows}, {cols}, {r2}, {c2});
    return out;
}}"""

translate = """\
{type} {func}({lvec} v) {{
    {type} out;
    {translate}(({scalar}*)&v, ({scalar}*)&out, {rows});
    return out;
}}"""

scale = """\
{type} {func}({lvec} v) {{
    {type} out;
    {scale}(({scalar}*)&v, ({scalar}*)&out, {rows});
    return out;
}}"""

# affine transformations for mat44
mat44rotate = """\
{type} {type}_rotate({lvec} r, {scalar} a) {{
    {scalar} c = cos(a), t = 1-c, s=sin(a);
    return ({type}) {{
        {{t*r.x*r.x + c, t*r.x*r.y + s*r.z, t*r.x*r.z - s*r.y, 0}},
        {{t*r.x*r.y - s*r.z, t*r.y*r.y + c, t*r.y*r.z + s*r.x, 0}},
        {{t*r.x*r.z + s*r.y, t*r.y*r.z - s*r.x, t*r.z*r.z + c, 0}},
        {{0, 0, 0, 1}}
    }};
}}"""

mat44perspective = """\
{type} {type}_perspective({scalar} angle, {scalar} aratio, {scalar} near, {scalar} far) {{
    {scalar} f = 1.0/tan(angle/2.0);
    return ({type}) {{
        {{f/aratio, 0, 0, 0}},
        {{0, f, 0, 0}},
        {{0, 0, (far+near)/(near-far), -1}},
        {{0, 0, 2*far*near/(near-far), 0}}
    }};
}}"""

add = """\
{type} {func}({type} a, {type} b) {{
    {type} out;
    {add}(({scalar}*)&a, ({scalar}*)&b, ({scalar}*)&out, {size});
    return out;
}}"""

sub = """\
{type} {func}({type} a, {type} b) {{
    {type} out;
    {sub}(({scalar}*)&a, ({scalar}*)&b, ({scalar}*)&out, {size});
    return out;
}}"""

smult = """\
{type} {func}({type} v, {rscalar} k) {{
    {type} out;
    {smult}(({scalar}*)&v, k, ({scalar}*)&out, {size});
    return out;
}}""";

interpolate = """\
{type} {func}({type} a, {type} b, {rscalar} t) {{
    {type} out;
    {interpolate}(({scalar}*)&a, ({scalar}*)&b, t, ({scalar}*)&out, {size});
    return out;
}}"""

dot = """\
{scalar} {func}({type} a, {type} b) {{
    return {dot}(({scalar}*)&a, ({scalar}*)&b, {size});
}}"""

# vec3 cross
vec3cross = """\
{type} {type}_cross({type} a, {type} b) {{
    return (vec3f) {{a.y * b.z - b.y * a.z, a.z * b.x - b.z * a.x, a.x * b.y - b.x * a.y}};
}}"""

sqlength = """\
{scalar} {func}({type} v) {{
    return {sqlength}(({scalar}*)&v, {size});
}}"""

length = """\
{rscalar} {func}({type} v) {{
    return {length}(({scalar}*)&v, {size});
}}"""

normalize = """\
{type} {func}({type} v) {{
    {type} out;
    {normalize}(({scalar}*)&v, ({scalar}*)&out, {size});
    return out;
}}"""

proj = """\
{lvec} {func}({type} v) {{
    {lvec} out;
    {proj}(({scalar}*)&v, ({scalar}*)&out, {size});
    return out;
}}"""

hom = """\
{lvec} {func}({type} v) {{
    {lvec} out;
    {hom}(({scalar}*)&v, ({scalar}*)&out, {size});
    return out;
}}"""

funcs = {
        "zero": zero,
        "identity": identity,
        "transpose": transpose,
        "mmult": mmult,
        "translate": translate,
        "scale": scale,
        "mat44rotate": mat44rotate,
        "mat44perspective": mat44perspective,
        "add": add,
        "sub": sub,
        "smult": smult,
        "interpolate": interpolate,
        "dot": dot,
        "vec3cross": vec3cross,
        "sqlength": sqlength,
        "length": length,
        "normalize": normalize,
        "proj": proj,
        "hom": hom
}
