from pathlib import Path
from time import perf_counter

from ..common.types import Results


def initialize():
    import itaxotools

    itaxotools.progress_handler("Initializing...")
    import core  # noqa
    import utils  # noqa


def execute(
    work_dir: Path,
    batch_mode: bool,
    input_query_path: Path,
    input_database_path: Path,
    input_query_list: list[Path],
    output_path: Path,
    blast_method: str,
    blast_evalue: float,
    blast_num_threads: int,
    append_multiple: bool,
    append_pident: float,
    append_length: int,
) -> Results:
    import itaxotools

    print(f"{batch_mode=}")
    print(f"{input_query_path=}")
    print(f"{input_database_path=}")
    print(f"{input_query_list=}")
    print(f"{output_path=}")
    print(f"{blast_method=}")
    print(f"{blast_evalue=}")
    print(f"{blast_num_threads=}")
    print(f"{append_multiple=}")
    print(f"{append_pident=}")
    print(f"{append_length=}")

    ts = perf_counter()

    if batch_mode:
        input_query_paths = input_query_list
    else:
        input_query_paths = [input_query_path]
    total = len(input_query_paths)

    for i, path in enumerate(input_query_paths):
        itaxotools.progress_handler(f"{i}/{total}", i, 0, total)
        execute_single(
            work_dir=work_dir,
            input_query_path=path,
            input_database_path=input_database_path,
            output_path=output_path,
            blast_method=blast_method,
            blast_evalue=blast_evalue,
            blast_num_threads=blast_num_threads,
            append_multiple=append_multiple,
            append_pident=append_pident,
            append_length=append_length,
        )
    itaxotools.progress_handler(f"{total}/{total}", total, 0, total)

    tf = perf_counter()

    return Results(output_path, tf - ts)


def execute_single(
    work_dir: Path,
    input_query_path: Path,
    input_database_path: Path,
    output_path: Path,
    blast_method: str,
    blast_evalue: float,
    blast_num_threads: int,
    append_multiple: bool,
    append_pident: float,
    append_length: int,
):
    from core import blast_parse, run_blast
    from utils import fastq_to_fasta, is_fastq, remove_gaps

    if is_fastq(input_query_path):
        target_query_path = work_dir / input_query_path.with_suffix(".fasta").name
        fastq_to_fasta(input_query_path, target_query_path)
        input_query_path = target_query_path

    blast_output_path = output_path / input_query_path.with_suffix(".out").name
    appended_output_path = output_path / input_query_path.with_stem(input_query_path.stem + "_with_blast_matches").name
    input_query_path_no_gaps = work_dir / input_query_path.with_stem(input_query_path.stem + "_no_gaps").name
    remove_gaps(input_query_path, input_query_path_no_gaps)

    run_blast(
        blast_binary=blast_method,
        query_path=input_query_path_no_gaps,
        database_path=input_database_path,
        output_path=blast_output_path,
        evalue=blast_evalue,
        num_threads=blast_num_threads,
        outfmt="6 length pident qseqid sseqid sseq qframe sframe",
        other="",
    )

    blast_parse(
        input_path=input_query_path,
        blast_result_path=blast_output_path,
        output_path=appended_output_path,
        database_name=input_database_path.stem,
        all_matches=append_multiple,
        pident_arg=append_pident,
        length_arg=append_length,
    )
