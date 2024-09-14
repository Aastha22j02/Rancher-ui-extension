import { IPlugin } from '@shell/core/types';

export const YOUR_PRODUCT_NAME = 'K8sGPTProduct';
export const BLANK_CLUSTER = '_';

export function init($plugin: IPlugin, store: any) {
  const {product} = $plugin.DSL(store, YOUR_PRODUCT_NAME);

  product({
    icon: 'gear',
    inStore: 'management',
    weight: 100,
    to: {
      name: `${ YOUR_PRODUCT_NAME }-c-cluster`,
      params: { product: YOUR_PRODUCT_NAME, cluster: BLANK_CLUSTER },
      meta: {
        product: YOUR_PRODUCT_NAME,
        cluster: BLANK_CLUSTER,
        pkg: YOUR_PRODUCT_NAME,
      },
    },
  });
}