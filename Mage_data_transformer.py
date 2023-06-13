if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):
    """
    Template code for a transformer block.

    Add more parameters to this function if this block has multiple parent blocks.
    There should be one parameter for each output variable from each parent block.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your transformation logic here
    laptop_data = data
    Laptop_Name_dim = laptop_data[['title','brand', 'model_name']]
    Laptop_Name_dim['Laptop_Name_id'] = Laptop_Name_dim.index

    laptop_feature_dim= laptop_data[['screen_size',
       'hard_disk_size','cpu_model','special_feature', 'graphics_card_description',
       'graphics_coprocessor', 'series', 'card_description', 'color',
       'cpu_speed', 'hard_disk_description', 'resolution', 'rating','price']]
    laptop_feature_dim['laptop_feature_id'] = laptop_feature_dim.index

    Ram_dim =laptop_data[['ram_memory_installed_size']].drop_duplicates().reset_index(drop= True)
    Ram_dim['Ram_os_id'] = Ram_dim.index

    os_dim = laptop_data[['operating_system']].drop_duplicates().reset_index(drop= True)
    os_dim['os_id'] = os_dim.index

    fact_details1 = laptop_data.merge(Laptop_Name_dim, on = 'title')\
                  .merge(os_dim, on = 'operating_system')\
                  .merge(Ram_dim, on = 'ram_memory_installed_size')\
                  .merge(laptop_feature_dim, on = ['screen_size',
       'hard_disk_size','cpu_model','special_feature', 'graphics_card_description',
       'graphics_coprocessor', 'series', 'card_description', 'color',
       'cpu_speed', 'hard_disk_description', 'resolution', 'rating','price'])\
        [['Laptop_Name_id','os_id','Ram_os_id','laptop_feature_id','price']]
    fact_details1['id'] = fact_details1.index

    print(fact_details1)
    return {"Laptop_Name_dim":Laptop_Name_dim.to_dict(orient = "dict"),
    "laptop_feature_dim":laptop_feature_dim.to_dict(orient = "dict"),
    "Ram_dim":Ram_dim.to_dict(orient = "dict"),
    "os_dim":os_dim.to_dict(orient = "dict"),
    "fact_details1":fact_details1.to_dict(orient = "dict")}



@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
