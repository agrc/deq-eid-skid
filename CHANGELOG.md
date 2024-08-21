# Changelog

## 1.0.0 (2024-08-21)


### Features

* implement publish and update for all tables ([128837d](https://github.com/agrc/deq-eid-skid/commit/128837d317556dbbf1f971c3a5e382a5547ae407))
* only send emails in the cloud ([a441721](https://github.com/agrc/deq-eid-skid/commit/a4417216f85b419895d4979c5d6dfd6eeccae40d))
* publish environmental incident layer ([83ae148](https://github.com/agrc/deq-eid-skid/commit/83ae1486bb3576345955880d149b3ba9646cd940))


### Bug Fixes

* convert to cloud run with higher timeout ([8cf7d82](https://github.com/agrc/deq-eid-skid/commit/8cf7d822368306ac921d80f9312e61922281530a))
* decrease service timeout to comply with gcp requirement ([de21805](https://github.com/agrc/deq-eid-skid/commit/de21805ea2ec7b27223f59eaf3ca4ad08fb87f65))
* increase memory limit ([18b9c8a](https://github.com/agrc/deq-eid-skid/commit/18b9c8a52a5213162c8bdd992e9c880a398edc35))
* memory suffix ([f108139](https://github.com/agrc/deq-eid-skid/commit/f1081393385d52d0bf574b92907ea2d0432d6422))
* move deps back to setup and remove functions ([e351a83](https://github.com/agrc/deq-eid-skid/commit/e351a834b783ae0446be84215266eaba38a4550d))
* move item ids to secrets to allow for different values per environment ([f7f3792](https://github.com/agrc/deq-eid-skid/commit/f7f37929508aed53f1b5184d79b46abef84d7bdd))
* pin requests to fix arcgis package issues ([983fd84](https://github.com/agrc/deq-eid-skid/commit/983fd84be7f4aff24f1c39e8959af4490046ec5a))
* run notify only if one of the deploy jobs succeeds ([f190150](https://github.com/agrc/deq-eid-skid/commit/f190150abb44d5ee66334f483ee124c706a10686))
* standardize workflows ([801b0fc](https://github.com/agrc/deq-eid-skid/commit/801b0fcf5c2e198a477464268bc630befbd61e2c))
* use correct input for service account ([2d5d999](https://github.com/agrc/deq-eid-skid/commit/2d5d9993d535cb4e43d31adde5d3307c2eebcdeb))
* use different table name and don't share in dev ([a7b7097](https://github.com/agrc/deq-eid-skid/commit/a7b70975a28c95d2e4e4aa41dcd9d6b94b5accc3))
* use generic email address ([61622b0](https://github.com/agrc/deq-eid-skid/commit/61622b0c1341131db870939e4b0cf1600e386523))


### Dependencies

* bump ci deps ([982aa8f](https://github.com/agrc/deq-eid-skid/commit/982aa8f6c2a67d391c0b7794b54d0c57e72def40))
* bump the major-dependencies group with 4 updates ([6d00457](https://github.com/agrc/deq-eid-skid/commit/6d00457bb46283dfc680b5074a00211022a57a8d))
* **dev:** update functions-framework requirement ([4f05e34](https://github.com/agrc/deq-eid-skid/commit/4f05e3484335b472b6dc1b32ba271acb8c0ddf59))
* update palletjack and pin supervisor ([fca212c](https://github.com/agrc/deq-eid-skid/commit/fca212c9423f09ac3e9fa72ae63c4b1c465995ee))


### Documentation

* add docstring to publish method ([4072de9](https://github.com/agrc/deq-eid-skid/commit/4072de94efd56843f570ded0793eaabecf8b5f30))
* add field mappings and view info ([432c37a](https://github.com/agrc/deq-eid-skid/commit/432c37ad7649b62f8f095f7fd2925280fcb85a53))
* add notes from Barry about field and api names ([24cc035](https://github.com/agrc/deq-eid-skid/commit/24cc035a7a76ec7aec46ee02d853557be173ba15))
* better local test command ([4afbe16](https://github.com/agrc/deq-eid-skid/commit/4afbe16031bcb415e245a802d328918f257f55e7))
* remove old function stuff and add note about publish method ([25eeb40](https://github.com/agrc/deq-eid-skid/commit/25eeb408fc96435b130aeaff2de7510c03ee0e87))
* start to make readme specific to this project ([e0b12dd](https://github.com/agrc/deq-eid-skid/commit/e0b12dd5c633bafec39017d7ac74b55616acb1b2))

## [1.0.0-4](https://github.com/agrc/deq-eid-skid/compare/v1.0.0-3...v1.0.0-4) (2024-08-16)


### Bug Fixes

* memory suffix ([aae5923](https://github.com/agrc/deq-eid-skid/commit/aae5923cd6e459c13555bc8aa1dc4e1a331c78e8))

## [1.0.0-3](https://github.com/agrc/deq-eid-skid/compare/v1.0.0-2...v1.0.0-3) (2024-08-16)


### Bug Fixes

* use correct input for service account ([db99809](https://github.com/agrc/deq-eid-skid/commit/db99809fe569f9d2e9e5646780e6f973fb4b90d2))

## [1.0.0-2](https://github.com/agrc/deq-eid-skid/compare/v1.0.0-1...v1.0.0-2) (2024-08-16)


### Bug Fixes

* decrease service timeout to comply with gcp requirement ([55bd0a7](https://github.com/agrc/deq-eid-skid/commit/55bd0a7efa12c8a868dad4105f3bb88d5fae415f))

## [1.0.0-1](https://github.com/agrc/deq-eid-skid/compare/v1.0.0-0...v1.0.0-1) (2024-08-16)


### Bug Fixes

* run notify only if one of the deploy jobs succeeds ([da2b8f8](https://github.com/agrc/deq-eid-skid/commit/da2b8f84ee999023e80e101589c749f7d7f40e62))

## 1.0.0-0 (2024-08-16)


### Features

* implement publish and update for all tables ([badeeb7](https://github.com/agrc/deq-eid-skid/commit/badeeb7020523501c2fa6405d0106ea821dbda0f))
* publish environmental incident layer ([d3a4e30](https://github.com/agrc/deq-eid-skid/commit/d3a4e30b3265569117a436757c76103e55745248))


### Bug Fixes

* move item ids to secrets to allow for different values per environment ([f9b3bb8](https://github.com/agrc/deq-eid-skid/commit/f9b3bb8729e86369c17c47691f07918924539c14))
* pin requests to fix arcgis package issues ([956cc04](https://github.com/agrc/deq-eid-skid/commit/956cc04a5a2e0211b93bf5039e85c9c3435bebef))
* standardize workflows ([611f939](https://github.com/agrc/deq-eid-skid/commit/611f93912a49270098f06599431c42da82b57a41))
* use different table name and don't share in dev ([74c8327](https://github.com/agrc/deq-eid-skid/commit/74c83276a9b60f26d720bff255c4e8223af5df9e))


### Dependencies

* bump ci deps ([982aa8f](https://github.com/agrc/deq-eid-skid/commit/982aa8f6c2a67d391c0b7794b54d0c57e72def40))
* bump the major-dependencies group with 4 updates ([6d00457](https://github.com/agrc/deq-eid-skid/commit/6d00457bb46283dfc680b5074a00211022a57a8d))
* **dev:** update functions-framework requirement ([4f05e34](https://github.com/agrc/deq-eid-skid/commit/4f05e3484335b472b6dc1b32ba271acb8c0ddf59))
* update palletjack and pin supervisor ([eeaee88](https://github.com/agrc/deq-eid-skid/commit/eeaee880979126410ef8e6a61454e935091d0fa9))


### Documentation

* add field mappings and view info ([581f94d](https://github.com/agrc/deq-eid-skid/commit/581f94daa0ea7d96fb4ec03e48a93f89a2861294))
* add notes from Barry about field and api names ([8383e81](https://github.com/agrc/deq-eid-skid/commit/8383e8151fcba07e4f6740bdb5df9aa6a2b4dfac))
* start to make readme specific to this project ([93cbe61](https://github.com/agrc/deq-eid-skid/commit/93cbe611e2e1b7bd9f4a0c1e469dcd6485f9f958))
