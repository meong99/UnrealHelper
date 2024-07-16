#pragma once
#include "CoreMinimal.h"
#include "Engine/DataAsset.h"
#include "DataAsset_ItemData.generated.h"

UCLASS()
class PROJECTCR_API UDataAsset_ItemData : public UDataAsset
{
    GENERATED_BODY()

public:
	UPROPERTY(BlueprintReadOnly, VisibleAnywhere)
	int64 ItemUID = 0;
	UPROPERTY(BlueprintReadOnly, VisibleAnywhere)
	FString ItemType = "";
};
