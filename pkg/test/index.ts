import { importTypes } from '@rancher/auto-import';
 
import { IPlugin } from '@shell/core/types';
 
import { BLANK_CLUSTER, YOUR_PRODUCT_NAME } from './product';
import Main from './pages/Main.vue';
 
// Init the package
export default function(plugin: IPlugin) {
  // Auto-import model, detail, edit from the folders
  importTypes(plugin);
 
  // Provide plugin metadata from package.json
  plugin.metadata = require('./package.json');
 
  // Load a product
  plugin.addProduct(require('./product'));
 
  plugin.addRoute({
    name: `${YOUR_PRODUCT_NAME}-c-cluster`,
    component: Main,
    path: `/${YOUR_PRODUCT_NAME}/c/cluster/test`,
    meta: {
      product: YOUR_PRODUCT_NAME,
      cluster: BLANK_CLUSTER,
      pkg: YOUR_PRODUCT_NAME
    }
  });
}