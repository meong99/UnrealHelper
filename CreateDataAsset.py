import unreal
import sys

# 패키지와 경로 설정
package_path = "/Game/Datas"
asset_name = f"{sys.argv[1]}"

# 패키지를 생성
package = unreal.EditorAssetLibrary.create_package(package_path)

# 블루프린트 클래스 생성
blueprint_factory = unreal.BlueprintFactory()
blueprint_factory.set_editor_property(f"{sys.argv[1]}", unreal.DataAsset)

blueprint_asset = unreal.AssetToolsHelpers.get_asset_tools().create_asset(
    asset_name,
    package_path,
    unreal.Class(None, f"{sys.argv[1]}"),
    blueprint_factory
)

# 변경 사항 저장
unreal.EditorAssetLibrary.save_asset(f"{package_path}/{asset_name}")
unreal.EditorAssetLibrary.sync_browser_to_objects([blueprint_asset])