const graph = require('./graph.json');
const research = require('./research.json');
const references = new Set(graph.nodes.flatMap(node => node.refs));
module.exports = { ...graph, sources: research.sources.filter(source => references.has(source.id)) };
