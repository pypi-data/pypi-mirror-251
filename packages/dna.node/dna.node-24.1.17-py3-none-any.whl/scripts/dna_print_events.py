from __future__ import annotations

from typing import Any
from contextlib import closing
import argparse

from kafka.consumer.fetcher import ConsumerRecord

from dna.event.kafka_utils import open_kafka_consumer, read_topics, PollTimeout
from scripts.utils import add_kafka_consumer_arguments, read_typed_topic


def define_args(parser) -> None:
    parser.add_argument("--files", nargs='+', default=None, help="track files to print")
    add_kafka_consumer_arguments(parser)
    parser.add_argument("--drop_poll_timeout", action='store_true')
    parser.add_argument("--type", choices=['node-track', 'global-track', 'json-event', 'track-feature'],
                        default=None,
                        help="event type ('node-track', 'global-track', 'json-event', 'track-feature')")
    parser.add_argument("--filter", metavar="expr", help="predicate expression", default=None)
  
     
def run(args:argparse.Namespace) -> None:
    filter = compile(args.filter, "<string>", 'eval') if args.filter is not None else None
    
    if args.files:
        from dna.event import read_pickle_event_file
        for file in args.files:
            for ev in read_pickle_event_file(file):
                if not filter or eval(filter, {'ev':ev}):
                    print(ev)
    else:
        options = vars(args)
        for rec in read_typed_topic(**options):
            match rec:
                case ConsumerRecord():
                    ev = rec.value
                    if not filter or eval(filter, {'ev':ev}):
                        print(ev)
                case PollTimeout():
                    print(rec)
                case _: pass

   
def main():
    parser = argparse.ArgumentParser(description="Print event file.")
    define_args(parser)
    
    args = parser.parse_args()
    run(args)

if __name__ == '__main__':
    main()