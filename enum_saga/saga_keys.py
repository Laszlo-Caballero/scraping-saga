from enum import Enum

class SagaKeys(Enum):
    PRODUCTS_ID = "testId-searchResults-products"
    PRODUCT_SELECTOR = 'data-testid="ssr-pod"'
    BRAND_CLASS = 'jsx-727486952.title1.secondary.jsx-233704000.bold.pod-title.title-rebrand'
    NAME_ID= 'testId-pod-displaySubTitle-'
    PRICES_CONTAINER_CLASS = 'jsx-3493300662.ol-4_GRID.pod-prices.fa--prices.li-separation'
    LOADER_CLASS = 'jsx-673020274.loader'
    TOTAL_PAGES_CONTAINER_ID = "testId-Pagination-Container-top"

class DetailsKeys(Enum):
    DETAIL_ID = 'product-b2c-ui'
    BREADCRUMB_CONTAINER_ID = 'data-testid="breadcrumbs"'
    SELLER_ID = 'testId-SellerInfo-sellerName'
    SPECTS_CONTAINER_ID = 'data-testid="product-top-specifications__list"'
    SPECTS_ACCORDEON_ID = 'productSpecificationsAccordion'
    SPECTS_CLASS_TABLE = 'jsx-513032616.specification-table'
    SHOW_MORE_SPECTS_BUTTON_CLASS = 'jsx-2445445216.accordion__show-more-btn'
    GALERY_CONTAINER_CLASS = 'jsx-4185066464.image-gallery-carousel__container'