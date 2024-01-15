import torch
from vbench import VBench

def register_subparsers(subparser):
    parser = subparser.add_parser('evaluate')
    parser.add_argument(
        "--output_path",
        type=str,
        default='./evaluation_results/',
        help="output path to save the evaluation results",
    )
    parser.add_argument(
        "--full_json_dir",
        type=str,
        default='./VBench_full_info.json',
        help="path to save the json file that contains the prompt and dimension information",
    )
    parser.add_argument(
        "--videos_path",
        type=str,
        required=True,
        help="folder that contains the sampled videos",
    )
    parser.add_argument(
        "--dimension",
        type=str,
        required=True,
        help="evaluation dimensions",
    )
    parser.add_argument(
        "--load_ckpt_from_local",
        type=bool,
        required=False,
        help="whether load checkpoints from local default paths (assuming you have downloaded the checkpoints locally",
    )
    parser.add_argument(
        "--read_frame",
        type=bool,
        required=False,
        help="whether directly read frames, or directly read videos",
    )
    parser.set_defaults(func=evaluate)

def evaluate(args):
    print(f'args: {args}')

    device = torch.device("cuda")
    my_VBench = VBench(device, args.full_json_dir, args.output_path)
    
    print(f'start evaluation')
    my_VBench.evaluate(
        videos_path = args.videos_path,
        name = args.dimension,
        dimension_list = [args.dimension],
        local=args.load_ckpt_from_local,
        read_frame=args.read_frame,
    )
    print('done')

