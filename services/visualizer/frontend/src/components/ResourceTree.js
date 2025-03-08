import React from 'react';
import Tree from 'react-d3-tree';

// Helper function to transform our data into the format expected by react-d3-tree
const transformData = (resources) => {
  const root = {
    name: 'GCP Resources',
    children: []
  };

  // Process compute resources
  if (resources.compute && resources.compute.length > 0) {
    const computeNode = {
      name: 'Compute',
      children: resources.compute.map(vm => ({
        name: vm.name,
        attributes: {
          type: vm.type,
          zone: vm.zone,
          id: vm.id
        }
      }))
    };
    root.children.push(computeNode);
  }

  // Process networking resources
  if (resources.networking && resources.networking.length > 0) {
    const networkNode = {
      name: 'Networking',
      children: resources.networking.map(net => ({
        name: net.name,
        attributes: {
          type: net.type,
          cidr: net.cidr,
          id: net.id
        }
      }))
    };
    root.children.push(networkNode);
  }

  // Process Kubernetes resources
  if (resources.kubernetes && resources.kubernetes.length > 0) {
    const kubernetesNode = {
      name: 'Kubernetes',
      children: resources.kubernetes.map(cluster => ({
        name: cluster.name,
        attributes: {
          location: cluster.location,
          version: cluster.version,
          id: cluster.id
        }
      }))
    };
    root.children.push(kubernetesNode);
  }

  return root;
};

const ResourceTree = ({ data }) => {
  const treeData = transformData(data);

  return (
    <div style={{ width: '100%', height: '500px' }}>
      <Tree 
        data={treeData} 
        orientation="vertical"
        pathFunc="step"
        collapsible={true}
        translate={{ x: 300, y: 50 }}
        zoom={0.8}
        nodeSize={{ x: 200, y: 100 }}
        separation={{ siblings: 2, nonSiblings: 2 }}
      />
    </div>
  );
};

export default ResourceTree;
