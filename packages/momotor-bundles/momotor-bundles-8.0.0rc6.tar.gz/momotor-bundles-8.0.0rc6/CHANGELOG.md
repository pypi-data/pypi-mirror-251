# Changelog

<!--next-version-placeholder-->

## v7.0.2 (2023-06-19)

### Fix

* Incorrect fetching of `executable` attribute ([`97653fa`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/97653fa866833acd0376fc4764a28473875a0ed6))

## v7.0.1 (2022-11-21)
### Fix
* Correctly handle empty directory attachments when exporting a bundle ([`a3cb87e`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/a3cb87efb079bd78a8a57ae2de458cc88287e1f8))

## v7.0.0 (2022-10-06)
### Feature
* Add `rglob` and `irglob` lookups to filters ([`3d694da`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/3d694da0ad6975d97a6c5308fb979951e2b10033))

### Fix
* Remove unnecessary requirement from requirements.txt ([`876970d`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/876970de92c812b278b7b4018eb9157cf29221db))
* Better handling of directory attachments ([`e15b079`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/e15b079b1243384bf066f78a302c3a59418a1774))

### Breaking
* File and Repository methods changes: ([`e15b079`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/e15b079b1243384bf066f78a302c3a59418a1774))

## v6.1.0 (2022-03-24)
### Feature
* Move recoding of content to bundle creation stage. Adds an argument `optimize`. Recoding is done with optimize is set. ([`c44c4e8`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/c44c4e822045b0a6c6055d208874387908c681a1))
* Add 'recode_content' argument to Result.recreate (closes #31) ([`801ff6b`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/801ff6b289fe5fa5770861329f499e7dcdf3b159))

## v6.0.1 (2022-01-20)
### Fix
* Removed deprecation for 'int' option type, added 'bool' and 'boolean' type ([`a144ef9`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/a144ef960d32f4ad1bf8b3df4f1ea3e7e8278067))

## v6.0.0 (2022-01-17)
### Feature
* Make Outcome a separate enum from OutcomeSimpleType, add OutcomeLiteral type ([`3d50a53`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/3d50a53d70e99e56399debdd3cacbf685fd4bb56))
* Add 'properties' argument to create_error_result_bundle ([`337284c`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/337284c36e9b4d7a99e6bf162a25cca65e50aec4))
* Add skip-if property checking ([`2ec1bec`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/2ec1bec8495faedeed41e799ae1f3e870de7ffbe))
* Add result filtering and matching functions from base checklet (closes #25) ([`ccfec9d`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/ccfec9d7817692b3ca46b31b89967fbebce9caa8))
* Add "skip" as value for task outcomes (closes #24) ([`aa6933e`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/aa6933e9abe7956ce370c65418445d184ef3e224))
* Add 'properties' argument to create_error_result_bundle ([`812bc61`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/812bc615a1944045f38562c942c90adddadea025))
* Add skip-if property checking ([`b829353`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/b82935342973b565d6a3eea2e65b1d46bd4b3701))
* Add result filtering and matching functions from base checklet (closes #25) ([`2428675`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/24286756dcb34fd4eccfa8864e97e9178805dbb6))
* Add "skip" as value for task outcomes (closes #24) ([`635b7f0`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/635b7f0b655f0c6cbd3bfe659f688a4025c5000e))

### Fix
* Correct typehint for `cls` ([`95bd649`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/95bd64910123292d4e01c1b19c867884958d8f8a))
* Add OutcomeLiteral type ([`c88109e`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/c88109e20d8f490a67b2412970679b9eb1618bbb))
* Use outcome directly (create accepts both enum and str) ([`06fe917`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/06fe9178e9125948f3f0e24e63c940e49a783dc9))
* Imports ([`1644ae7`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/1644ae73aa31fc25b93fa5fec92f5553cd4dd961))
* Create_error_result_bundle() function ([`5ee5048`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/5ee5048281914b264d90453c5a691997171ae6f7))
* Add "test**" id query feature ([`d3e7c37`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/d3e7c370758915ac744b276e9961b544e9639b50))
* Use `outcome_enum` in passed/failed/skipped/erred properties to validate outcome value before comparing ([`4bf371b`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/4bf371b7c7feec600785e9f98bb46cb9e57aad1c))
* Use outcome directly (create accepts both enum and str) ([`54d067f`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/54d067fcb745abbc01dcd47b6a6b9c5c8e211e2b))
* Imports ([`35e5c47`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/35e5c47622bc7f4532bad5bdf12fb2eda332491f))
* Create_error_result_bundle() function ([`e02b295`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/e02b295d508008dfd94a4bde0a4070a9ab72cdfd))
* Add "test**" id query feature ([`2b768fe`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/2b768fec07c81699d36a1f243e066aa5dee31f86))
* Use `outcome_enum` in passed/failed/skipped/erred properties to validate outcome value before comparing ([`57ad63e`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/57ad63e6c55ebb3f3554b85de327d65fb9b041bf))

### Breaking
* Several modules have moved to another package ([`5e15ea3`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/5e15ea3a1544da38b746e04a12c3424955056f56))
* Several modules have moved to another package ([`6034cbb`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/6034cbb46cfd43de26a3f75565b07ae152226bcf))

## v5.2.0 (2021-12-30)
### Feature
* Add "skip" as value for task outcomes (closes #24) ([`7fd8a7f`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/7fd8a7f1f334e465d5e0f418bd55567c34ef5fed))

### Fix
* Use outcome directly (create accepts both enum and str) ([`64bbadf`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/64bbadf94dff7430c499a971e28fe2cbbdf745ad))
* Use `outcome_enum` in passed/failed/skipped/erred properties to validate outcome value before comparing ([`30c1abf`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/30c1abfc168f930ae7c3d4d1c250de6aca6b79e3))

## v5.1.2 (2021-12-21)
### Fix
* Only raise InvalidDependencies for explicit dependencies, not for wildcard or placeholder ones ([`7f737e6`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/7f737e6d3765660f211495503452b7ede48a8394))

## v5.1.1 (2021-11-26)
### Fix
* If `executable` attribute is a string value, convert it to boolean ([`0d46c05`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/0d46c05652bee309c5ec1f323ed03108749a3f8a))

## v5.1.0 (2021-11-23)
### Feature
* Add wildcard dependencies and ignore dependencies with arithmetic errors ([`b553f6a`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/b553f6a3488e6b3848cf8528177ea4477cbcf3e2))
* Add simple arithmetic to `apply_task_number` ([`0390416`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/03904162ced5b45b6a33599e4c42cad85e736560))

### Fix
* _get_full_deps ([`44553e8`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/44553e844d4d88df4bd369a8d629463069cc4c10))
* Changed dependency calculation methods to return a tuple instead of a set, to maintain step ordering ([`f5a02ee`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/f5a02ee10e7d265274f3cf0efe0faecf6b8494c1))

## v5.0.0 (2021-11-19)
### Feature
* Make `FilesType` public ([`003a359`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/003a3599f74d07dbdf4e488e713e50f2bd50fc29))
* Made `apply_task_number` public and added `make_result_id_re` ([`9c5ab14`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/9c5ab14dc14839cba4b94cdb2de5c4bb4b8384bf))
* Add task utility methods `task_number_from_id` and `task_id_from_number` ([`3e66a83`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/3e66a838ec24a31964d8a64335b19e677cb386a0))
* When recreating a result, allow changing the step_id ([`93b049d`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/93b049d1db2849d330b00b75ed000db9000054bb))
* Add types for locations and providers ([`db36dde`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/db36dde59080f0c4780fafd25df1169719fa7ccc))
* Changes to dependencies and tasks methods ([`b5832f0`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/b5832f0d081487aa2a4c44e8dfa0ccec84aa5b4b))
* Support multiple tasks per step ([`3841148`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/3841148996e45d16395d68261468816cb381fdde))

### Fix
* Self.depends can be None ([`2ab3196`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/2ab3196ac48c87af41e0841eacc294fbdb7fcc99))
* Get_task_dependencies() returned incorrect mapping ([`7984431`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/798443155c37aa79e3a3b1b964f7932fcd4a803a))
* KeyedTuple.get() raises KeyError when item does not exist ([`cee605a`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/cee605a777f2163b22c28e2482234aab4d31b525))
* Cleanup and optimization ([`034475e`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/034475e14f5a8ef84445669437f5ea0e6458b0cb))
* Typing ([`e09129c`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/e09129cc26ec28f4602925e1834965ca02f48974))
* Relax XML dependency and result step-id types ([`28c388a`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/28c388ae255a9ccc76a9482661d92b2e221a4ee2))
* Install xsdata[cli] in development ([`fcfc65c`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/fcfc65cd3254f77c5253d38b309cd3e3b68508a4))
* More verbose file exceptions ([`ba6de38`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/ba6de386519e9f497f239ab2299df7b5d5eaddc7))
* Period in step-id is not a problem ([`4f4fc78`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/4f4fc78f8a0d2ee01b50835f0c341c4f7ab8a7ec))
* Unit tests ([`ddab49b`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/ddab49b90edde9f655eca5e73ac213f22e45ddc3))
* Clearer assertion error messages ([`e3ac2ca`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/e3ac2ca6693491987f5cd1f1758038dccc89bd59))

### Breaking
* interface of `momotor.bundles.utils` package changed to support task ids  ([`3841148`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/3841148996e45d16395d68261468816cb381fdde))

## v4.1.0 (2021-09-23)
### Feature
* Make exported attachment file names pure ASCII (closes #21) ([`244edef`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/244edef5b3aaab11e276a1144374a37562f0a099))

## v4.0.3 (2021-09-14)
### Fix
* Do not strip trailing whitespace from quopri encoded inline content ([`023da26`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/023da2640f25ae626bbc98e308611d9be8e762ec))

## v4.0.2 (2021-08-21)
### Fix
* Tests for directories in zip bundles ([`256755e`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/256755e05ac17d6a70d6beb08939d6685583e262))
* If path validation fails silently, set path to None ([`26cae68`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/26cae685cc231c9f390dd0b6e802495949da1ba1))
* Added `legacy` argument to factory arguments, only ignore checklet src errors when legacy mode is enabled ([`79175d5`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/79175d5a4d88d56d8a437a3c72ab7f2ca08342c2))

## v4.0.1 (2021-08-20)
### Fix
* Result nodes may contain checklets with invalid `src` attribute ([`227258d`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/227258d6cce058158438cb9de3bced0bbb7a4c26))
* Honour the `validate_signature` setting when creating checklet element from node ([`6c10099`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/6c10099ad315a539a7803c3e54e3adb1de1c0b8e))

## v4.0.0 (2021-08-17)
### Feature
* Add `Bundle.detect` ([`4988f57`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/4988f577ba2f617d81d95a65052dbad8d9989ea1))
* Add `condition` to `Outcome` for the common use case where a bool needs to be converted into an outcome ([`2c01d38`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/2c01d38594db25b531e71ab7dbc8a20342f7a612))
* Support Decimal values as alternatives to floats ([`dc98e5c`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/dc98e5c34e410ea042b8bf440e69cf194e2b60b4))
* Add `enable` field to OptionDefinition ([`e95cacf`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/e95cacfd5ee10c50db00a2e40bb2f39ea21fc4c9))
* Warn about missing attachments if `validate_signature` is False ([`16d0512`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/16d051242f0a29d8caf0b2dd5604fca636e48191))
* Validate attachment paths on creation ([`9250262`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/92502626ae0acdde65fc85a549cdb4ffc703b33b))
* Allow renaming in the recreate method ([`de8e4cb`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/de8e4cbcfa82edeb6ed0e141c709aa6b6643fd99))
* Update xsdata dependency to version 21.7 ([`604ff41`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/604ff41f2852534e8ad22e2bc6ad0c45d7d8c66d))
* Always convert `name` attribute for content nodes into a `PurePosixPath` ([`8334fe4`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/8334fe47e02c2e0a3b67444a3b6e96d5e226f72d))
* Implement ~ operator for All() and Any() filters ([`b421a5f`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/b421a5f2da236ae2f69e668a8a7bf5e8828dc82d))
* Move and rename `Result.OutcomeType` to `Outcome` for easier imports ([`35f0c33`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/35f0c333b2459494b6c68114a3a4b8f9a62593f6))
* Added 'legacy' option to write XML compatible with the old parser ([`506e93c`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/506e93cdf44721f2363f932a08eb98fc90a13b04))
* Implement hash validation on bundle load ([`bde7fd6`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/bde7fd6cf51a1be635c129c6e752ebe8d5d704c5))
* Add BundleFactoryArguments ([`c4c1338`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/c4c13387b6f770fa44f59d854aa4e0c7fbae59cc))
* Implement checklet.repository attachments ([`f4a6f34`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/f4a6f34ef55bcd395d0fa657f78e604ba9b3ae3d))
* Add `size`, `executable` and hashing attributes to file nodes ([`f098321`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/f098321701b2f8c5a8becf75126c4b4d37793f80))
* Create dataclasses for the bundle creation options and provide the options to the deeper _construct* methods ([`4899c0d`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/4899c0dedb9b6a2281b16c01024a3d444f939c4a))
* Support referencing files in another bundle (for recreate) ([`477c8b2`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/477c8b2a2693efc4039cc62dbc17fef6bf916bfc))
* Rewrite files and attachments system (WIP) ([`047f8ca`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/047f8ca11953fac79af2fc2eaea786e4072f46d1))
* File handling changes ([`4bae2d3`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/4bae2d3718713f83e33b796f80c45ae02ea9a1b3))
* Change handling of content nodes ([`3bc4b82`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/3bc4b82cac9f31cd8bd9abd256f3e092c5b2efee))
* Recipes have files at the top level ([`7ecfc1d`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/7ecfc1ddfb7f8cc52e64ec555d7af55e48a7a2e0))
* Update options ([`fd100c2`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/fd100c220e46d4aaa3be8f0b315708fec2433cfd))
* Handle subdomains in OptionDefinition.resolve ([`14dcb46`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/14dcb463a5769ff68d32b56c819148559a8ccc87))
* Changed inheritance of option domains, added test cases ([`598e4f4`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/598e4f4391b29891f5af3b8288f7cf75498fb23e))
* Implement OptionDefinition. Based on StepOption from version 0 step base ([`bb48dbd`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/bb48dbd5cd9dd293b9fcbf6c941eb4e1d36d02f5))
* Remove <options> from <depends> nodes ([`bbb4a9a`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/bbb4a9ae17e51ca7369252fd58cecef6ed63182c))
* Drop unused 'external' attribute from option nodes ([`456c1b6`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/456c1b6d589c7d85ba9471d2940201b0db05210b))
* Add types for sequences of options/properties/resources. the getters always return a sequence ([`0d1a818`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/0d1a8180afee29ed447c657f20013d420cc74714))
* Result.outcome property accepts both strings and OutcomeSimpleTypes ([`0e843ba`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/0e843ba8d1600e2de1b66450bf6949e311bfc9e3))
* Add Checklet.get_dist_name() ([`fbf64a4`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/fbf64a4912a79411dfdb2a3c60264f9ea9d7dfbd))
* Use FilterableTuple for file functions ([`66a5666`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/66a56669a62c85c20e1501906369a69104ac9418))
* Use FilterableTuple for all sequences of elements ([`8bef5a6`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/8bef5a620d22f1f6df687514cf2293af7a8e84bb))
* Ingest the filtering from momotor-common, modified, added documentation ([`0bb1455`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/0bb1455156dffaf785c510b8da75f099a42f9505))
* Ingest step_condition.py from base checklet ([`d2cbddf`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/d2cbddfc78d60d67c81014154e167cab19be1f38))
* Make bundles immutable and unify interfaces ([`d16c9f5`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/d16c9f56291764e2083d3a102d8bde838d043348))

### Fix
* Typing.Literal is Python 3.8+ ([`399f4f3`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/399f4f37faf93064124e2e8fc02d11acf69715d5))
* `has_inline_content` could be incorrect if content was not processed ([`e6eba4d`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/e6eba4db3083802bd32dd90fcd18f93d42fbb17d))
* Correct handling of numeric properties ([`20a0dc6`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/20a0dc61256ab402e4fc869b55832d687191b824))
* Various fixes and enhancements for `make_matcher_fn` ([`fa81d0e`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/fa81d0e6b143816fae3cce87ea1a363f52d22ca6))
* Create directory as documented ([`282b01a`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/282b01a231c29cc740205b632fdb7e9067bd1061))
* Unused import ([`bc3db17`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/bc3db17d2fafd19f623214df610bce1d7e8ffaf6))
* Attachment linking ([`6c7a6aa`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/6c7a6aa67e322e38fea531f5a97787c323841813))
* Results attribute should never be `None` ([`8247e8c`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/8247e8cef19e56b7e2244cd5967a265d1b967f7d))
* Unused target_basesrc argument ([`5f92c82`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/5f92c82d80ac254c25777ee16f2697f344f522e2))
* Typing.Protocol is Python 3.8+ ([`828e9e1`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/828e9e18d62e7c4ad96b5b674e3e395ba8999a04))
* Cast Path-like objects to strings, convert to posix paths if possible ([`e3d66d3`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/e3d66d36a59d9cfa1eed31f37435e4d8abe3f9c8))
* Provide default checklet.entrypoint value ([`87fa1ab`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/87fa1aba50f5a81b541074e12681c22ce3b4a670))
* Correctly export directory attachments ([`ed7abda`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/ed7abdafefeff203e538ae2291d917be46085db5))
* Add missing parent node ([`304c6d2`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/304c6d2fc6ae7a7ecc614feb025c973ded8e20f4))
* Make `export_src` read-only, allow multiple calls to `_export_path()` ([`5147f2b`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/5147f2baa9923e4dc38c333d89607ed6adba15eb))
* Empty attachment nodes ([`6add05d`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/6add05d0edeadb3503023aee44758d3063b0f3d8))
* Handle name arguments ([`9b7bebb`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/9b7bebb5336a48214b33e3962652b9999c25b08f))
* Setting `executable` attribute from file mode doesn't work on Windows, so just require it to always be manually set ([`3a174b1`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/3a174b1229a97677fa053584305d5d6e8868f0fb))
* Add missing attachments.rst ([`94e7852`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/94e7852a2f538a2a3902f522505a7feef31d73f5))
* Prevent import error when lxml is not installed ([`7c6b4f6`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/7c6b4f607ec04c3a01efdd9a136840fd2aa485e4))
* Recipe.steps and Recipe.tests always return a KeyedTuple. Setting Recipe.tests should be ignored instead of throwing an exception ([`688e0ac`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/688e0ac3032bd6c39f22a83374df9d6d90dc4d45))
* More deprecated imports ([`85466f2`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/85466f29a938ff3d85f7838ab9c71f69a799e59f))
* Deprecated imports ([`7d3b5aa`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/7d3b5aa5cd981ded39779205b5f2da6a70881307))
* Skip doctest with known SyntaxError ([`0b696a8`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/0b696a8a3c3d7bb02e1810ba98cfb129e608a7ab))
* Typing.final import in Python 3.7 ([`0754dca`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/0754dca3730ccb117230ded5afe4e663011a6941))
* Move DEFAULT_DOMAIN into Options class ([`d9e89c0`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/d9e89c04412e44b8890650bfd3e04eaab39b007d))
* Add Result.outcome_enum ([`1441a9a`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/1441a9ab483c0aaa7cb027ee2a0046379690318f))

### Breaking
* semantics of option domain inheritance has changed  ([`598e4f4`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/598e4f4391b29891f5af3b8288f7cf75498fb23e))
* Removes unused <options> from <depends>  ([`bbb4a9a`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/bbb4a9ae17e51ca7369252fd58cecef6ed63182c))
* bundles are now immutable. List attributes are now tuples, setters raise an exception when called twice  ([`d16c9f5`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/d16c9f56291764e2083d3a102d8bde838d043348))

## v3.4.0 (2021-04-23)
### Feature
* Bump xsdata version to ==21.4 ([`52704ef`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/52704ef3b389e7ead93804bf89d32efb64a4ba31))

## v3.3.4 (2021-03-30)
### Fix
* Throw `InvalidDependencies` exception when steps depend on non-existent steps (fixes #20) ([`9204d6b`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/9204d6b4d2e44e8ab3bdebbaf6c5ad3b2d85cce5))

## v3.3.3 (2021-02-11)
### Fix
* __doc__ is not available when running Python with the -OO option ([`3443a3f`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/3443a3ff002d7c261821cb804df645da65935f3f))

## v3.3.2 (2021-02-02)
### Fix
* Update xsdata version requirement in setup.py ([`7792b5a`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/7792b5a7bb252f8b48400ecae2657027884f7a91))

## v3.3.1 (2021-02-02)
### Fix
* Update xsdata to 21.1, undo workarounds (Closes #18) ([`a1ccd2c`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/a1ccd2cebb6a49153d5b9bffb08812c0ce0e63ed))

## v3.3.0 (2020-12-17)
### Feature
* Update to xsdata 20.12 ([`90da816`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/90da816bc5d4f1d69e96aff99e627d37811e7bd0))

## v3.2.2 (2020-12-10)
### Fix
* Also work around #18 when creating from node ([`586b748`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/586b7484dab3acfdb4f34351aff9feb024e9d148))

## v3.2.1 (2020-12-10)
### Fix
* Workaround for issue in `xsdata` that tries to convert an attribute value to a QName if it starts with a '{' ([`cdbb172`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/cdbb1727ace9c39a094e627b0f2b0cfad1351bfa))

## v3.2.0 (2020-12-07)
### Feature
* Drop unused `momotor.bundles.utils.content` ([`fa7db1b`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/fa7db1b044e0e699496ae10d9374376b906cf9ff))
* Implement XML validation ([`199a4db`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/199a4db1adf80a0e29b47b8f416e36f46a3ae65e))
* Replace pyxb with xsdata lib ([`bb04bab`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/bb04babba57b10724773b17e8b4bc1f7ad6e3d09))
* Replace all pxby related imports ([`05fe125`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/05fe1257629bacf05d03ede5ce851e2be58c27a5))
* Replace pxyb install with xsdata ([`5907c56`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/5907c56442d3624e36262d3515aae6249ce3eb09))

### Fix
* Correct namespace ([`11af2f4`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/11af2f4f316c3089ca36312a510eb2e4980d92f2))
* Collecting properties ([`975c9c8`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/975c9c8b0f6ec47597087bd811fd7a0402210a95))
* Correct conversion to and from wildcard attributes ([`1fe986a`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/1fe986a009d1747bf581b6e313abfcdc59ddd12f))
* Correct conversion to and from checklet link/index/repository/package-version elements ([`7da5343`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/7da53439a6cdc11d6d4c29f38422b713e4e6608d))
* Implement missing method ([`dda46d3`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/dda46d3ab7508aea3da8ba2eb61a19e906070c9b))
* Typing.Final ([`4529fc0`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/4529fc047e28725018e11aa698064db5d9341db4))
* Xsdata version requirement ([`42f7068`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/42f7068eba04ce1c6ffe83fb2b6c6df07543a853))
* Return a dict of tuples from group_by_attr [skip-ci] ([`b01b007`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/b01b007bbf2c8b212b870ca1e601c23601988584))
* Group_by_attr should return a normal dict, not a defaultdict [skip-ci] ([`e1e9fce`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/e1e9fce9c357904aa476c9104f8ca8ac10983f6f))

## v3.1.0 (2020-11-02)
### Feature
* Add ElementMixinProtocol to help with static type checking of mixins ([`cc514ab`](https://gitlab.tue.nl/momotor/engine-py3/momotor-bundles/-/commit/cc514ab0be3d3f540e8118604207e8c3c2a19446))
