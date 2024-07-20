#pragma once
#include "CoreMinimal.h"
#include "DataAssets/DDDataAsset_DataAssetBase.h"
#include "DataAsset_ItemData.generated.h"

UCLASS()
class PROJECTCR_API UDataAsset_ItemData : public UDDDataAsset_DataAssetBase
{
    GENERATED_BODY()

public:
	UPROPERTY(BlueprintReadOnly, VisibleAnywhere)
	int64 ItemUID = 0;
	UPROPERTY(BlueprintReadOnly, VisibleAnywhere)
	FString ItemType = "";
};
