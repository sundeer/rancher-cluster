from invoke import Collection

from tasks import cluster, rancher, utils

namespace = Collection()
namespace.add_collection(cluster)
namespace.add_collection(rancher)
namespace.add_collection(utils)
