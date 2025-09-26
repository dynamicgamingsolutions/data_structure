/*This is the Master Insert query for Dynamic Gaming Solutions LLC.
This query pulls relevant data from 
    dbo.assets,
    dbo.cabinet,
    dbo.casino_name,
    dbo.revenue,
    dbo.state,
    dbo.theme,
    dbo.Tribe_name,
    dbo.vendor
and inserts it into dbo.Master_Revenue, used by the analytics team to review and visualize the state of our cabinet and theme footprint.

Best practice is to run this query as each casino sends in their revenue reports, and to run it for the previous month.
Unless a project has been done for a casino, all information outside of "revenue" will be static.

In the event that a project has been done for a casino, update the necessary tables before running this query.

Aspects involving
    theme,
    casino where a cabinet is located,
    par,
    denom,
    and ZBL location
will be updated in dbo.assets.

Aspects involving
    Commission ID,
    House WPU,
    and salesperson
will be updated in dbo.casino_name.

Please contact Paul Collins if any other information needs to be updated.

Originally created by: Buddy Harlin
Last Modified: 05/15/2025 by: Paul Collins
*/

/*Remove comment to push into MSSQL Database*/
-- INSERT INTO [DGS_SLOT].[dbo].[Master_Revenue]

--Select options
Select
    r.date, -- Date from "revenue"
    tribe.tribe_name, -- Tribe Name from "tribe"
    cn.casino_name, -- Casino Name from "casino_name"
    s.state, -- State from "state"
    a.asset_id, -- Asset ID from "assets"
    a.serial_number, -- Serial Number from "assets"
    v.vendor_name, -- Vendor Name from "vendor"
    cab.cabinet, -- Cabinet from "cabinet"
    theme.theme, -- Theme from "theme"
    a.par, -- Par from "assets"
    a.denom, -- Denom from "assets"
    r.coin_in, -- Coin In from "revenue"
    r.actual_win, -- Actual Win from "revenue"
    r.coin_in*(a.par*.01)Theo, -- Theo from "revenue"
    cast (round(r.actual_win/r.days_on_floor,2)as float)ADW, -- Convert the Actual Daily Win
    cast(round((r.coin_in*(a.par*.01))/r.days_on_floor,2)as float)TDW, -- Convert the Theo Daily Win
    r.days_on_floor, -- Days on Floor from "revenue"
    a.convert_date, -- Convert Date from "assets"
    a.performance_expire, -- Performance Expire from "assets"
    a.parts_expire, -- Parts Expire from "assets"
Case
When a.Class = 'II' then (r.days_on_floor * a.Class2_fee)
Else 0
END AS 'Class 2 Fee', -- Class 2 Fee from "assets"
    a.Class, -- Class from "assets"
    a.ZBL_location, -- ZBL Location from "assets"
    a.removal_date, -- Removal Date from "assets"
    a.active, -- Active from "assets"
    a.install_date, -- Install Date from "assets"
    cn.salesperson, -- Salesperson from "casino_name"
    r.promo, -- Promo from "revenue"
    a.Commission_ID, -- Commission ID from "casino_name"


/*Commission IDS
    1 at 20%
    2 at 18%
    3 at 18.8%
    4 at 20% minus $1 per day
    5 at 16.45% minus $3.50 per day
    6 at 20% minus $2.50 per day
    7 at 20% minus $1.44 per day
    8 at 19%
    9 at 20% minus $0.25 per day
    10 at 19% minus $1.50 per day
    11 at 20% minus 6% of actual win plus promo
    12 at 15%
    13 at 20% minus 8.75% of actual win plus rebate
    14 greater of 20% or $1
    15 20% with no loss passed on
    16 $65 a day rent
    17 Lessor of $35 a day minimum
    18 Lessor of 20% or $50 a day
    19 20% with a $60 a day maximum
    20 $55 a day rent
    21 at 15% minus $2 a day
    22 20% with a $65 Cap
    23 $45 a day rent
    24 17% with a $60 Cap
    25 20% with a $50 Cap
    26 20% with a %40 Cap
    27 15% with no loss passed
    28 $50 a day rent*/

Case
When a.Commission_ID = 1 then (r.Actual_Win) *.2
When a.Commission_ID = 2 then r.Actual_Win *.18
When a.Commission_ID = 3 then r.Actual_Win *.188
When a.Commission_ID = 4 then (r.Actual_Win *.2)-(r.Days_on_Floor*1)
When a.Commission_ID = 5 then (r.Actual_Win *.1645)-(r.Days_on_Floor*3.5)
When a.Commission_ID = 6 then (r.Actual_Win *.2)-(r.Days_on_Floor*2.5)
When a.Commission_ID = 7 then (r.Actual_Win *.2)-(r.Days_on_Floor*1.44)
When a.Commission_ID = 8 then r.Actual_Win *.19
When a.Commission_ID = 9 then (r.Actual_Win *.2)-(r.Days_on_Floor*.25)
When a.Commission_ID = 10 then ((r.Actual_Win *.19))-(r.Days_on_Floor*1.50)
When a.Commission_Id = 11 then (r.Actual_Win - ((r.Actual_win*.06)+promo))*.2
When a.Commission_Id = 12 then (r.Actual_Win *.15)
When a.Commission_ID = 13 then ROUND(((actual_win * .2)-((actual_win*.2)*.02))*1.075,2)
When a.Commission_ID = 14 then 
    CASE WHEN (r.Actual_Win*.2)>1 THEN (r.Actual_Win*.2) ELSE 1 END
When a.Commission_ID = 15 then 
    CASE WHEN (r.Actual_Win)>0 THEN (r.Actual_Win*.2) ELSE 0 END
When a.Commission_ID = 16 then r.days_on_floor * 65
When a.Commission_ID = 17 then 
    CASE WHEN (r.days_on_floor * 35)<(r.actual_win * .2) THEN (r.actual_win * .2) ELSE (r.days_on_floor * 35) END
When a.Commission_ID = 18 then
    CASE 
        WHEN r.actual_win < 0 THEN 0
        WHEN (r.actual_win * .2) < (r.days_on_floor * 50) THEN (r.actual_win * .2)
        ELSE (r.days_on_floor * 50) 
    END
When a.Commission_ID = 19 then
    CASE 
        WHEN (r.actual_win * .2) > (r.days_on_floor * 60) 
        THEN(r.days_on_floor * 60)
        ELSE (r.actual_win * .2)
    END
When a.Commission_ID = 20 then r.days_on_floor * 55
When a.Commission_Id = 21 then (r.Actual_Win *.15)-(days_on_floor*2)
When a.Commission_ID = 22 then
    CASE 
        WHEN (r.actual_win * .2) > (r.days_on_floor * 65) 
        THEN(r.days_on_floor * 65)
        ELSE (r.actual_win * .2)
    END
When a.Commission_ID = 23 then r.days_on_floor * 45
When a.Commission_ID = 24 then
    CASE 
        WHEN (r.actual_win * .17) > (r.days_on_floor * 60) 
        THEN(r.days_on_floor * 60)
        ELSE (r.actual_win * .17)
    END
When a.Commission_ID = 25 then
    CASE 
        WHEN (r.actual_win * .20) > (r.days_on_floor * 50) 
        THEN(r.days_on_floor * 50)
        ELSE (r.actual_win * .20)
    END
When a.Commission_ID = 26 then
    CASE 
        WHEN (r.actual_win * .20) > (r.days_on_floor * 40) 
        THEN(r.days_on_floor * 40)
        ELSE (r.actual_win * .20)
    END
When a.Commission_ID = 27 then 
    CASE WHEN (r.Actual_Win)>0 THEN (r.Actual_Win*.15) ELSE 0 END
When a.Commission_ID = 28 then r.days_on_floor * 50
Else 0
end as Commission,

Case
When  a.Commission_ID = 2  then r.days_on_floor *2
--When  a.Commission_ID = 6  then r.days_on_floor *2.5
else 0
end As Billed_Fees,
ca.main_house_average, -- House WPU from "casino_name"
GETDATE()



FROM [DGS_SLOT].[dbo].[assets] as a -- Lable "assets" as "a"

Inner join

[DGS_SLOT].[dbo].[revenue] r -- Lable "revenue" as "r"


on a.serial_number = r.serial_number -- Join "assets" and "revenue" on "serial_number"

inner join

[DGS_SLOT].[dbo].[casino_name] as cn -- Lable "casino_name" as "cn"

on cn.casino_id = r.casino_id -- Join "casino_name" and "revenue" on "casino_id"

inner join

[DGS_SLOT].[dbo].[vendor] as v -- Lable "vendor" as "v"

on v.vendor_id = a.vendor_id -- Join "vendor" and "assets" on "vendor_id"

inner join

[DGS_SLOT].[dbo].[cabinet] as cab -- Lable "cabinet" as "cab"

on

cab.cabinet_id = a.cabinet_id -- Join "cabinet" and "assets" on "cabinet_id"

Inner join

[DGS_SLOT].[dbo].[theme] as theme -- Lable "theme" as "theme"

on

theme.theme_id = a.theme_id -- Join "theme" and "assets" on "theme_id"

inner join

[DGS_SLOT].[dbo].[Tribe_name] tribe -- Lable "Tribe_name" as "tribe"

on

tribe.tribe_id = cn.tribe_id -- Join "Tribe_name" and "casino_name" on "tribe_id"

inner join

[DGS_SLOT].[dbo].[state] as s -- Lable "state" as "s"

on   s.state_id = cn.state_id -- Join "state" and "casino_name" on "state_id"

inner join

[clients].[dbo].[casinos] as ca
on cn.casino_name = ca.casino_short

/*User must update Casino ID and Date on next two lines*/

Where (
    cn.casino_name LIKE '%Indigo Sky%'
    )
AND r.casino_id = a.casino_id
AND r.[date] = '2025-08-31'

-- AND r.days_on_floor = 11

-- AND r.serial_number = '13096013'
ORDER By ZBL_location