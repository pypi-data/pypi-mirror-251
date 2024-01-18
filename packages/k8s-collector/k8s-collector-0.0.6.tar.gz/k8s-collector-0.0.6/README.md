# k8s-collector
collect k8s objects, parse them with jmespath and send them to sink

## How to run
`k8s-collector` collectors package with built-in objects named `Collector`s.  
`Collector` encapsulates all the necessary parts of the library for specific collection usage, for example `K8SCollector` collects k8s resources.  
For now the `k8s-collector` library used to collect k8s resources, but in theory you can define `Listener`, `Handler`, `Processor`, `Filterer` and `Sink` for everything
and thus creating `Collector` for everything.

### K8SCollector
To use `K8SCollector` simply run

```python
python -m k8s_collector.collectors.K8SCollector
```
to use namespaced version provide `-n/--namespace` argument
```python
python -m k8s_collector.collectors.K8SCollector -n second-namespace
```