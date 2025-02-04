from pathlib import *
import json, sys, EthorenllProgress


def d():
    input_dir = Path(sys.argv[2])
    output_dir = Path(sys.argv[3])

    output_dir.mkdir(exist_ok=True)


    files = input_dir.glob("*")

    for f in files:
        if f.is_dir():
            continue;
        print("Processing: ", f)
        result = EthorenllProgress.decode(f)

        with open(Path(output_dir, f.stem + ".json"), 'w', encoding='utf-8') as file:
            file.write(json.dumps(result, indent=4, ensure_ascii=False))


def e():

    input_dir = Path(sys.argv[2])
    json_dir = Path(sys.argv[3])
    output_dir = Path(sys.argv[4])
    output_dir.mkdir(exist_ok=True)

    files = input_dir.glob("*")

    for f in files:
        if f.is_dir():
            continue;
        print("Processing: ", f)

        EthorenllProgress.encode(f, Path(json_dir, f.stem + ".json"), Path(output_dir, f.name))


if __name__ == "__main__":
    if sys.argv[1] == "decode":
        d()
    elif sys.argv[1] == "encode":
        e()
    else:
        print("Invalid command")