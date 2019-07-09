from utils import scalarType

def funcName(t, n):
    return "generic_{0}_{1}".format(t, n)

def funcBody(t, n):
    data = {
            "func": funcName(t, n),
            "type": t,
            "scalar": scalarType(t)
    }
    for f,v in funcs.items(): data[f] = funcName(t, f)
    return funcs[n].format(**data)

def getFuncs():
    return funcs

zero = """\
static void {func}({type} *out, size_t n) {{
    for(size_t i = 0; i < n; i++) out[i] = 0;
}}"""

identity = """\
static void {func}({type} *out, size_t n) {{
    {zero}(out, n*n);
    for(size_t i = 0; i < n; i++) out[i*n + i] = 1;
}}"""

transpose = """\
static void {func}({type} *m, {type} *out, size_t n) {{
    for(size_t i = 0; i < n; i++)
        for(size_t j = 0; j < n; j++)
            out[j*n + i] = m[i*n + j];
}}"""

mmult = """\
static void {func}({type} *a, {type} *b, {type} *out, size_t r1, size_t c1, size_t r2, size_t c2) {{
    for(size_t i = 0; i < r1; i++)
        for(size_t j = 0; j < c2; j++)
            for(size_t k = 0; k < c1; k++)
                out[i*c2 + j] += a[i*c1 + k] * b[k*c2 + j];
}}"""

translate = """\
static void {func}({type} *v, {type} *out, size_t n) {{
    {identity}(out, n);
    for(size_t i = n-2; i >=0; i--) out[(n-1)*n + i] = v[i];
}}"""

scale = """\
static void {func}({type} *v, {type} *out, size_t n) {{
    {identity}(out, n);
    for(size_t i = n-2; i >= 0; i--) out[i*n + i] = v[i];
}}"""

add = """\
static void {func}({type} *a, {type} *b, {type} *out, size_t n) {{
    for(size_t i = 0; i < n; i++) out[i] = a[i] + b[i];
}}"""

sub = """\
static void {func}({type} *a, {type} *b, {type} *out, size_t n) {{
    for(size_t i = 0; i < n; i++) out[i] = a[i] - b[i];
}}"""

smult = """\
static void {func}({type} *v, {scalar} k, {type} *out, size_t n) {{
    for(size_t i = 0; i < n; i++) out[i] = v[i] * k;
}}"""

interpolate = """\
static void {func}({type} *a, {type} *b, {scalar} t, {type} *out, size_t n) {{
    {sub}(b, a, out, n);
    {smult}(out, t, out, n);
    {add}(a, out, out, n);
}}"""

dot = """\
static {type} {func}({type} *a, {type} *b, size_t n) {{
    {type} res = 0;
    for(size_t i = 0; i < n; i++) res += a[i] * b[i];
    return res;
}}"""

sqlength = """\
static {type} {func}({type} *v, size_t n) {{
    return {dot}(v, v, n);
}} """

length = """\
static {scalar} {func}({type} *v, size_t n) {{
    return sqrt({sqlength}(v, n));
}}"""

normalize = """\
static void {func}({type} *v, {type} *out, size_t n) {{
    {scalar} l = 1.0/{length}(v, n);
    {smult}(v, l, out, n);
}}"""

proj = """\
static void {func}({type} *v, {type} *out, size_t n) {{
    for(size_t i = n-2; i >= 0; i--) out[i] = v[i];
}}"""

hom = """\
static void {func}({type} *v, {type} *out, size_t n) {{
   {scalar} h = v[n-1];
   for(size_t i = n-2; i >=0; i--) out[i] = v[i]/h;
}}"""

funcs = {
        "zero": zero,
        "identity": identity,
        "transpose": transpose,
        "mmult": mmult,
        "translate": translate,
        "scale": scale,
        "add": add,
        "sub": sub,
        "smult": smult,
        "interpolate": interpolate,
        "dot": dot,
        "sqlength": sqlength,
        "length": length,
        "normalize": normalize,
        "proj": proj,
        "hom": hom
}
