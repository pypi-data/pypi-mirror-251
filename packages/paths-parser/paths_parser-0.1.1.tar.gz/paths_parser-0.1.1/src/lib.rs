use pyo3::prelude::*;

use nom::IResult;
use nom::character::complete as c;
use nom::sequence::{tuple, delimited, terminated};
use nom::bytes::complete::tag;
use nom::multi::many0;

fn parse_tuple(input: &str) -> IResult<&str, (i64, i64)> {
    let (rem, (_, res1, _, res2, _)) = tuple((tag("("), delimited(c::space0, c::i64, c::space0), tag(","), delimited(c::space0, c::i64, c::space0), tag(")")))(input)?;
    Ok((rem, (res1, res2)))
}

fn parse_line(input: &str) -> IResult<&str, Vec<(i64, i64)>> {
    let (rem, (mut res, res1)) = tuple((many0(terminated(parse_tuple, delimited(c::space0, tag(","), c::space0))), parse_tuple))(input)?;
    res.push(res1);
    Ok((rem, res))
}

fn parse_whole(input: &str) -> IResult<&str, Vec<Vec<(i64, i64)>>> {
    let (rem, (mut res, res1)) = tuple((many0(terminated(parse_line, c::line_ending)), parse_line))(input.trim())?;
    res.push(res1);
    Ok((rem, res))
}

/// Formats the sum of two numbers as string.
#[pyfunction]
fn parse(x: &str) -> PyResult<Vec<Vec<(i64, i64)>>> {
    Ok(parse_whole(x).unwrap().1)
}

/// A Python module implemented in Rust.
#[pymodule]
fn paths_parser(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(parse, m)?)?;
    Ok(())
}

#[test]
fn test() {
    let tmp = parse_whole("(1, 2), (3, 4)
(5, 6)
(7, 8), (9, 10)



").unwrap();
    println!("{:?}", tmp);
}