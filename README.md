Convert Cargo.lock to the [DOT] format for rendering with [GraphViz].

```
$ ./cargo-lock-to-dot.py Cargo.lock --interesting=foo,bar | dot -Tsvg > depgraph.svg
```

The optional `--interesting` flag specifies crates to be visually highlighted.

[GraphViz]: http://www.graphviz.org
[DOT]: https://en.wikipedia.org/wiki/DOT_%28graph_description_language%29
