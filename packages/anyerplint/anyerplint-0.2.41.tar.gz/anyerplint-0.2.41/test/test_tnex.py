import pytest
from anyerplint.ast import FuncCall
from anyerplint.tnex import ParseError, parse, translate_str


def test_parser() -> None:
    assert parse("foo") == "foo"
    assert parse("foo(1;1)") == FuncCall("foo", ["1", "1"])

    assert parse("foo(1;;1)") == FuncCall("foo", ["1", "", "1"])
    assert parse("foo(1; 1)") == FuncCall("foo", ["1", "1"])
    assert parse("foo(1; ;1)") == FuncCall("foo", ["1", "", "1"])
    assert parse('foo(1; "1")') == FuncCall("foo", ["1", "", '"1"'])

    assert parse('"some string"') == '"some string"'
    assert parse('"foo";0') == '"foo"', "0"
    assert parse("foo(1);2") == FuncCall("foo", ["1"])
    assert parse('foo("some string";"other string";0)') == FuncCall(
        "foo", ['"some string"', '"other string"', "0"]
    )

    assert parse('foo("some string";"other string");1') == FuncCall(
        "foo", ['"some string"', '"other string"']
    )

    # nothing special with ,
    assert parse("a,b(c,d;e,f;1.0)") == FuncCall("a,b", ["c,d", "e,f", "1.0"])

    assert parse(r'" string with \" char"') == '" string with \\" char"'
    assert (
        parse(r'"some string with ) and ( and \" characters"')
        == '"some string with ) and ( and \\" characters"'
    )

    assert parse(r'foo,"long / () accessor"') == 'foo,"long / () accessor"'
    assert parse(r'foo(F,NOW(),"yyyy")') == FuncCall(
        "foo", [FuncCall(',"yyyy"', [FuncCall("F,NOW", [])])]
    )
    assert parse(r'F,NOW(),"yyyy"') == FuncCall(',"yyyy"', [FuncCall("F,NOW", [])])

    complex = parse(
        r'foo(f1;bar(b1;b2;"b3";"wide string");f2;baz(1;"some string with ) and ( and \" characters")));top1'
    )
    assert complex == FuncCall(
        "foo",
        [
            "f1",
            FuncCall("bar", ["b1", "b2", '"b3"', '"wide string"']),
            "f2",
            FuncCall("baz", ["1", '"some string with ) and ( and \\" characters"']),
        ],
    )

    with pytest.raises(ParseError, match="Unterminated string"):
        parse('foo("unterminated)')
    with pytest.raises(ParseError, match="Empty parse result for expression: ';'"):
        parse(";")
    with pytest.raises(ParseError, match="Empty parse result for expression: ''"):
        parse("")


def test_translate_syntax() -> None:
    assert (
        translate_str(
            'F,EVAL(obj.A,AssetCode;=;"";F,EVAL(obj.A,SUM;"&gt;";"0";40;50);F,EVAL(obj.A,SUM;"&gt;";"0";70;75))'
        )
        == '(obj.A,AssetCode = "" ? (obj.A,SUM > "0" ? 40 : 50) : (obj.A,SUM > "0" ? 70 : 75))'
    )

    assert (
        translate_str(
            "F,EVAL(F,EXISTS(v;config);=;1;F,REPLACE(F,LOWER(v,config);rootconfig;systemvars);&quot;&quot;)"
        )
        == '(defined(config) = 1 ? v,config.lower().replace(rootconfig -> systemvars) : "")'
    )
